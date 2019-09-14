import asyncio
import io
from dataclasses import dataclass
from .stack import task_print_stack


@dataclass
class Node:
    name: str
    state: str
    traceback: str
    task: str = None


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
