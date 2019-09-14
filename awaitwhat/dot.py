import asyncio
import io
import json
import re

from dataclasses import dataclass

from .blocker import blockers
from .stack import task_print_stack
from .node import Node


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


def build_node(task, current):
    if isinstance(task, asyncio.Task):
        buf = io.StringIO()
        data = task_print_stack(task, None, buf)
        try:
            name = task.get_name()
        except AttributeError:
            name = "Task"
        # FIXME can we ever see a "done" task?
        if task.done():
            state = "done"
        else:
            state = "current" if task is current else "pending"
        return Node(name, state, buf.getvalue(), task)
    elif isinstance(task, asyncio.Future):
        return Node("Future", None, None, task)
    else:
        return Node(str(task), None, None, task)


def describe(task, current=None):
    node = build_node(task, current)
    if isinstance(node.task, asyncio.Task):
        label = concise_stack_trace(f"{node.name} {node.state}\n{node.traceback}")
    else:
        label = concise_other(str(node.task))
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


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

    PREFIX = '\n        '
    stops = {task: blockers(task) for task in tasks}
    nodes = set(sum(stops.values(), list(stops.keys())))
    nodes = PREFIX.join(f"{id(node)} {describe(node, current)}" for node in nodes)
    edges = PREFIX.join(
        f"{id(task)} -> {', '.join(str(id(task_to_wait)) for task_to_wait in tasks_to_wait)}"
        for task, tasks_to_wait in stops.items()
    )

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {nodes}
        {edges}
    }}
    """.strip()
