import asyncio
import what


thecoro = None


def poke(coro):
    try:
        if not coro.cr_frame:
            raise Exception("coro has no frame")
        print(coro.__name__, "lasti", coro.cr_frame.f_lasti)
        rv = what.next(coro.cr_frame)
        # print("value", rv)
        return rv
    except Exception as e:
        print(":(", e, coro)
    print()


def foretrace(coro):
    while coro:
        coro = poke(coro)


async def tester():
    await asyncio.sleep(0.1)
    foretrace(thecoro)

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
