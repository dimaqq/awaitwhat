import asyncio
import json
import re

from dataclasses import dataclass

from .blocker import blockers
from .node import Node, build_node
from .utils import concise_stack_trace, concise_other


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
