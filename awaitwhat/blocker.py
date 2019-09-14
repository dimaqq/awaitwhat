import inspect
import random


def blockers(task):
    """What does this task wait for?"""
    w = task._fut_waiter
    if not w:
        return [f'<Not blocked {random.random()}>']
    # asyncio.gather()
    try:
        # ideally check `w` type
        return w._children
    except AttributeError:
        pass
    # FIXME shield should be shown as a frame on the top of the stack
    # asyncio.shield()
    try:
        # ideally check if it's an `_outer_done_callback`
        callback, _ctx = w._callbacks[0]
        return [inspect.getclosurevars(callback).nonlocals["inner"]]
    except (AttributeError, TypeError, IndexError):
        pass
    # FIXME other awaitables
    return [w]
