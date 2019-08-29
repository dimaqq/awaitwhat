def blockers(task):
    """What does this task wait for?"""
    w = task._fut_waiter
    if not w:
        return
    try:
        # asyncio.gather()
        return w._children
    except AttributeError:
        pass
    # FIXME other awaitables
    return [w]
