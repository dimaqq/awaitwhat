import inspect

# work in progress:

# when a task is ultimately waiting on gather(), _done_callback is visible.


def decipher_done_callback(done_callback):
    closure = inspect.getclosurevars(done_callback).nonlocals
    state = f"progress: {closure['nfinished']}/{closure['nfuts']}"
    future = closure["outer"]
    print(future, state)
    children = closure["children"]
    for child in children:
        if child.done():
            # resolved, exception, cancelled
            if child.cancelled():
                print(child, "cancelled")
            elif child.exception():
                print(child, child.exception())
            else:
                print(child, child.result())
        else:
            print(child, "pending")


def task_callback(t):
    # FIXME: there may be several; py 3.8 vs py 3.7
    return t._callbacks[0][0]
