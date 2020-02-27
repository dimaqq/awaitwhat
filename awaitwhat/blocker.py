import inspect
import random
from . import sleep
from .stack import task_get_stack


def blockers(task):
    """What does this task wait for?"""
    waiter = task._fut_waiter
    if not waiter:
        return [f"<Not blocked {random.random()}>"]

    stack = task_get_stack(task, None)

    if len(stack) > 2 and sleep.mine(stack[-2]):
        return [sleep.decode(stack[-2])]

    # asyncio.gather()
    try:
        # ideally check `w` type
        return waiter._children
    except AttributeError:
        pass

    # FIXME shield should be shown as a frame on the top of the stack
    # asyncio.shield()
    try:
        # ideally check if it's an `_outer_done_callback`
        callback, _ctx = waiter._callbacks[0]
        return [inspect.getclosurevars(callback).nonlocals["inner"]]
    except (AttributeError, TypeError, IndexError):
        pass

    # FIXME other awaitables
    return [waiter]
