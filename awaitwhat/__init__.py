from asyncio.base_tasks import _task_print_stack, _task_get_stack
import types
from . import _what
from . import gather


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


# FIXME: what order is the stack in, as in, is it reversed?
def extend_stack(s, limit=None):
    stack = s[:]
    while isinstance(stack[-1], types.FrameType):
        if limit is not None and limit > len(stack):
            break
        try:
            n = _what.next(stack[-1])
        except Exception as e:
            n = str(e)
        try:
            f = n.cr_frame
        except Exception as e:
            # FIXME this should be something that prints like frame
            f = FakeFrame(f"{n}: {e}")
        stack.append(f)
    return stack


def task_get_stack(task, limit):
    stack = _task_get_stack(task, limit)
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
    return _task_print_stack(Wrapper(task), limit, file)


# FIXME: what can be awaited:
#
# - coro (done)
# - Task (enumerated, but needs a bridge)
# - Future (naked, unclear who ought to resolve it)
# - Event (e.wait() is a coro, but needs a bridge?)
# - gather (via callback)
# - shield (via callback)
# - asyncio.run (via callback)
#
# - TaskWakeupMethWrapper (via callback)
# - bridge FutureIter to Future (or just rely on Task wait_for=<...>

# FIXME: callbacks:
#
# top-level event loop thing:
# cb=[_run_until_complete_cb() at /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/base_events.py:158
#
# gather:
# cb=[gather.<locals>._done_callback() at /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/asyncio/tasks.py:664
#
# shield:
# ...
