from __future__ import annotations
import asyncio
import io
import itertools
import json
import re
from .blocker import blockers
from .stack import task_print_stack


def concise_stack_trace(trace):
    def clean(line):
        if line.startswith("Stack for "):
            return
        if '"<Sentinel>"' in line:
            return
        if re.search('File ".*/site-packages/.*"', line):
            line = re.sub('[^"]*/site-packages/', "", line)
        if re.search('File ".*/lib/python[0-9][.][0-9]/.*"', line):
            line = re.sub('[^"]*/lib/python[0-9][.][0-9]/', "", line)
        return line

    return "\n".join(filter(None, (clean(l) for l in trace.split("\n"))))


def concise_other(other):
    if other.startswith("<Future "):
        return "Future"
    return other


def describe(task, current=None):
    if isinstance(task, asyncio.Task):
        buf = io.StringIO()
        data = task_print_stack(task, None, buf)
        try:
            name = task.get_name()
        except AttributeError:
            name = "Task"
        if task.done():
            state = "done"
        else:
            state = "current" if task is current else "pending"
        label = concise_stack_trace(f"{name} {state}\n{buf.getvalue()}")
    else:
        label = concise_other(str(task))
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def graph(tasks, current=None) -> Tuple[Set[Task], Set[Tuple[Task, Task]]]:
    """
    Computes a graph of Tasks and awaitables.
    Returns:
    * a set of all graph nodes
    * a set of edges (a, b) where a waits for b
    """

    # dot format requires a node as target of an edge
    counter = itertools.count()
    stops = {t: blockers(t) or [f"<Not blocked {next(counter)}>"] for t in tasks}
    nodes = set(sum(stops.values(), list(stops.keys())))
    edges = set((k, v) for k, vv in stops.items() for v in vv)
    return nodes, edges


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    # dot format requires a node as target of an edge
    try:
        current = asyncio.current_task()
    except RuntimeError:
        current = None

    nodes, edges = graph(tasks, current=current)
    nodes = "\n        ".join(f"{id(t)} {describe(t, current)}" for t in nodes)
    edges = "\n        ".join(f"{id(e[0])} -> {id(e[1])}" for e in edges)

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {nodes}
        {edges}
    }}
    """.strip()
