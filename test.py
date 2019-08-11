import asyncio
import what


d = dict()


def poke(coro, text="what?"):
    print(text, coro.__name__)
    try:
        if not coro.cr_frame:
            raise Exception("coro has no frame")
        print("lasti", coro.cr_frame.f_lasti)
        rv = what.next(coro.cr_frame)
        print("value", rv)
    except Exception as e:
        print(":(", e)
    print()


async def foo():
    return 42 + (88 * (3 + (await bar()) + (await bar())))


async def main():
    return await asyncio.gather(foo(), foo())


async def bar():
    poke(c, "down")
    return 1


c = main()
poke(c, "way before")
asyncio.run(c)


# TODO
#
# When a coro is blocked on gather(), the thing on the stack is:
# <_asyncio.FutureIter object at 0x1086b1040>
#
# This is because instruction preceding YIELD_FROM is GET_AWAITABLE
# Which converts Future into an iterator:
#
# https://github.com/python/cpython/blob/51aac15f6d525595e200e3580409c4b8656e8a96/Modules/_asynciomodule.c#L1633
