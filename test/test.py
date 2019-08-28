import asyncio
import awaitwhat
import sys


def trace_all_tasks():
    print("### Python native task stack traces")
    for t in asyncio.Task.all_tasks():
        asyncio.base_tasks._task_print_stack(t, None, sys.stdout)
        print()

    print("### Extended task stack traces")
    for t in asyncio.Task.all_tasks():
        awaitwhat.task_print_stack(t, None, sys.stdout)
        print()

    tt = asyncio.Task.all_tasks()
    t = list(tt)[0]
    print(t)
    cb = awaitwhat.gather.task_callback(t)
    try:
        awaitwhat.gather.decipher_done_callback(cb)
    except Exception as e:
        print("failed to decipher", e)
    __import__("pdb").set_trace()


async def tester():
    await asyncio.sleep(0.1)
    trace_all_tasks()


async def job():
    await foo()


async def foo():
    await bar()


async def bar():
    await baz()


async def baz():
    await leaf()


async def leaf():
    await asyncio.sleep(1)


async def work():
    await asyncio.gather(tester(), job())


asyncio.run(work())


# TODO
#
# When a coro is blocked on gather(), the thing on the stack is:
# <_asyncio.FutureIter object at 0x1086b1040>
#
# This is because instruction preceding YIELD_FROM is GET_AWAITABLE
# Which converts Future into an iterator:
#
# https://github.com/python/cpython/blob/51aac15f6d525595e200e3580409c4b8656e8a96/Modules/_asynciomodule.c#L1633
