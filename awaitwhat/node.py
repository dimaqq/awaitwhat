import asyncio
import io
from dataclasses import dataclass
from .stack import task_print_stack
from .utils import concise_stack_trace
from .blocker import blockers


@dataclass
class Node:
    name: str
    state: str
    traceback: str
    task: str = None

    def __hash__(self):
        return hash(self.task)

    def __eq__(self, other):
        return self.task == other.task


@dataclass
class Edge:
    source_node: Node
    dest_node: Node


def build_node(task, current):
    if isinstance(task, asyncio.Task):
        buf = io.StringIO()
        task_print_stack(task, None, buf)
        try:
            name = task.get_name()
        except AttributeError:
            name = "Task"
        if task.done():
            state = "done"
        else:
            state = "current" if task is current else "pending"
        return Node(name, state, concise_stack_trace(buf.getvalue()), task)
    elif isinstance(task, asyncio.Future):
        return Node("Future", None, None, task)
    else:
        return Node(str(task), None, None, task)


def build_nodes_and_edges(tasks):
    try:
        current = asyncio.current_task()
    except RuntimeError:
        current = None

    stops = {task: blockers(task) for task in tasks}
    nodes = set()
    edges = list()
    for task, tasks_to_wait in stops.items():
        source_node = build_node(task, current)
        nodes.add(source_node)
        for task_to_wait in tasks_to_wait:
            dest_node = build_node(task_to_wait, current)
            nodes.add(dest_node)
            edges.append(Edge(source_node, dest_node))

    return nodes, edges
