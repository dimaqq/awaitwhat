import asyncio
import logging
import types
import what


thecoro = None


def frames(coro):
    while coro:
        try:
            yield f"{coro.__name__} ip {coro.cr_frame.f_lasti}"
        except Exception as e:
            yield str(coro)
            return

        try:
            coro = what.next(coro.cr_frame)
        except Exception as e:
            yield str(e)
            return


def foretrace(coro):
    for line in frames(coro):
        print(line)
    print()


def print_stack(s):
    for f in s:
        print(f)


def extended_stack(s):
    stack = s[:]
    while isinstance(stack[-1], types.FrameType):
        try:
            n = what.next(stack[-1])
        except Exception as e:
            n = str(e)
        try:
            f = n.cr_frame
        except Exception as e:
            f = f"{n}: {e}"
        stack.append(f)
    return stack


def trace_all_tasks():
    for t in asyncio.Task.all_tasks():
        print("----task-----")
        # for frame in t.get_stack():
        for frame in extended_stack(t.get_stack()):
            print(frame)
        print()


async def tester():
    await asyncio.sleep(0.1)
    foretrace(thecoro)
    trace_all_tasks()

async def leaf(): await asyncio.sleep(1)
async def baz(): await leaf()
async def bar(): await baz()
async def foo(): await bar()
async def job(): await foo()

async def work():
    global thecoro
    thecoro = job()
    await asyncio.gather(tester(), thecoro)

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
