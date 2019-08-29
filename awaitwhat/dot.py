import asyncio
import io
import json
import random
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
        # FIXME can we ever see a "done" task?
        state = "current" if task is current else "pending"
        label = concise_stack_trace(f"{name} {state}\n{buf.getvalue()}")
    else:
        label = concise_other(str(task))
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
    stops = {t: blockers(t) or [f"<Not blocked {random.random()}>"] for t in tasks}
    nodes = set(sum(stops.values(), list(stops.keys())))
    nodes = "\n        ".join(f"{id(t)} {describe(t, current)}" for t in nodes)

    edges = "\n        ".join(
        f"{id(k)} -> {', '.join(str(id(v)) for v in vv)}" for k, vv in stops.items()
    )

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {nodes}
        {edges}
    }}
    """.strip()
