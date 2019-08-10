import asyncio
import what


cc = [None]


def poke(coro, text="what?"):
    print("++++++++++++++")
    print(text)
    try:
        if coro.cr_frame:
            rv = what.next(coro.cr_frame)
            print(rv)
        else:
            print("coro has no frame")
    except Exception as e:
        print(e)
    print("--------------")


async def main():
    c = foo()
    cc[0] = c
    poke(c, "before")
    await c
    poke(c, "after")


async def foo():
    x = 12
    await asyncio.sleep(0.1)
    c = cc[0]
    poke(c, "inside")
    await asyncio.sleep(0.1)
    return x + 34
    # t = asyncio.create_task(bar())
    # await t


async def bar():
    await asyncio.sleep(0.1)


asyncio.run(main())
