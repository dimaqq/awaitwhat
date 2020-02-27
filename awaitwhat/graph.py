from __future__ import annotations
import asyncio
import io
from dataclasses import dataclass
from .stack import task_print_stack
from .utils import concise_stack_trace
from .blocker import blockers


@dataclass
class Vertex:
    name: str
    state: str
    traceback: str
    task: str = None

    def __hash__(self):
        return hash(self.task)

    def __eq__(self, other):
        return self.task == other.task

    @classmethod
    def build(cls, task, current):
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
            return cls(name, state, concise_stack_trace(buf.getvalue()), task)
        elif isinstance(task, asyncio.Future):
            return cls("Future", None, None, task)
        else:
            return cls(str(task), None, None, task)


@dataclass
class Edge:
    src: Vertex
    dst: Vertex


def build(tasks) -> Tuple[Set[Vertex], List[Edge]]:
    try:
        current = asyncio.current_task()
    except RuntimeError:
        current = None

    stops = {task: blockers(task) for task in tasks}
    vertices = set()
    edges = list()

    for who, what in stops.items():
        src = Vertex.build(who, current)
        vertices.add(src)
        for blocker in what:
            dst = Vertex.build(blocker, current)
            vertices.add(dst)
            edges.append(Edge(src, dst))

    return vertices, edges
