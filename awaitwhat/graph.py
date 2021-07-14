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
        src = Vertex.new(who, current)
        vertices.add(src)
        children = blockers(who)
        if len(children) > 1 and isinstance(children[1], asyncio.Task):
            # This is a wait_for task
            # We get two vertices, one for wait_for(dst1)
            # and other for the awaitable that wait_for 
            # awaits on(dst2)
            dst1 = Vertex.new(children[0], current)
            dst2 = Vertex.new(children[1], current)
            vertices.add(dst1)
            vertices.add(dst2)
            edges.append(Edge(src, dst1))
            edges.append(Edge(dst1, dst2))
            continue
        for what in blockers(who):
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
    def new(cls, task, current):
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


@dataclass(frozen=True)
class Edge:
    src: Vertex
    dst: Vertex
