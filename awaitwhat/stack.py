""" Shows what a coroutine waits for """
import asyncio
import types
from . import _what


class FakeCode:
    co_filename = "<Sentinel>"
    co_name = None

    def __init__(self, name):
        self.co_name = name


class FakeFrame:
    f_lineno = 0
    f_globals = None

    def __init__(self, name):
        self.f_code = FakeCode(name)


def extend_stack(s, limit=None):
    stack = s[:]
    while stack and isinstance(stack[-1], types.FrameType):
        if limit is not None and limit >= len(stack):
            break
        try:
            n = _what.next(stack[-1])
        except Exception as e:
            n = str(e)
        try:
            f = n.cr_frame
        except Exception as e:
            f = FakeFrame(f"{n}: {e}")
        stack.append(f)
    return stack


def task_get_stack(task, limit):
    stack = asyncio.base_tasks._task_get_stack(task, limit)
    if limit is None or len(stack) < limit:
        # FIXME should the stack be extended if there's an exception?
        stack = extend_stack(stack, limit)
    return stack


class Wrapper:
    def __init__(self, task):
        self.task = task

    def __str__(self):
        return str(self.task)

    def __repr__(self):
        return repr(self.task)

    @property
    def _exception(self):
        return self.task._exception

    def get_stack(self, limit=None):
        # FIXME, should the stack be extended if there's an exception?
        return task_get_stack(self.task, limit)


def task_print_stack(task, limit, file):
    return asyncio.base_tasks._task_print_stack(Wrapper(task), limit, file)
