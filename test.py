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


async def main():
    poke(c, "before")
    d["f"] = foo()
    poke(d["f"], "before")
    42 and (await d["f"]) or 34
    poke(d["f"], "after")
    poke(c, "after")
    await asyncio.sleep(0.1)


async def foo():
    await asyncio.sleep(0.1)
    poke(c, "inside")
    poke(d["f"], "inside")
    print(42 + (13 * (poke(d["f"], "arithmetic") or 1) * 2) + 32)
    99 and (await bar()) or 78
    await asyncio.sleep(0.1)


async def bar():
    poke(c, "deep inside")
    poke(d["f"], "deep inside")
    print(asyncio.all_tasks())
    await asyncio.sleep(0.1)

c = main()
poke(c, "way before")
asyncio.run(c)
