from __future__ import annotations
import asyncio
import io
from dataclasses import dataclass
from .stack import task_print_stack
from .utils import concise_stack_trace
from .blocker import blockers


def new(tasks) -> Tuple[Set[Vertex], List[Edge]]:
    try:
        current = asyncio.current_task()
    except RuntimeError:
        current = None

    vertices = set()
    edges = list()

    for who in tasks:
        children = blockers(who)
        src = Vertex.new(
            who, current, extra_text=[c for c in children if isinstance(c, str)]
        )
        vertices.add(src)
        for what in children:
            dst = Vertex.new(what, current)
            vertices.add(dst)
            edges.append(Edge(src, dst))

    return vertices, edges


@dataclass(frozen=True)
class Vertex:
    name: str
    state: str
    traceback: str
    task: str = None

    def __hash__(self):
        return hash(self.task)

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.task == other.task

    @classmethod
    def new(cls, task, current, *, extra_text=()):
        extra = "\n".join(extra_text)
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
            traceback = "\n".join(
                filter(None, (concise_stack_trace(buf.getvalue()), extra))
            )
            return cls(name, state, traceback, task)
        elif isinstance(task, asyncio.Future):
            return cls("Future", None, extra, task)
        else:
            return cls(str(task), None, extra, task)


@dataclass(frozen=True)
class Edge:
    src: Vertex
    dst: Vertex
