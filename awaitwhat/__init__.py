from asyncio.base_tasks import _task_print_stack, _task_get_stack
import types
from . import _what
from . import gather
from . import stack
from . import dot
from . import blocker
from . import helpers

# FIXME: shorter to do
#
# - mock up a run - 3xTask - coro - 3xTask - naked Future scenario
#
# - report Task id's (everywhere)
# - bridge _GatheringFuture to children (Tasks)
#
# - unwrap TaskWakeupMethWrapper (work forwards)
# or
# - ungather leaf gather calls (work backwards)

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


# TODO
#
# When a coro is blocked on gather(), the thing on the stack is:
# <_asyncio.FutureIter object at 0x1086b1040>
#
# This is because instruction preceding YIELD_FROM is GET_AWAITABLE
# Which converts Future into an iterator:
#
# https://github.com/python/cpython/blob/51aac15f6d525595e200e3580409c4b8656e8a96/Modules/_asynciomodule.c#L1633
