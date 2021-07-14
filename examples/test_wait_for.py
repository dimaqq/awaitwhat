import asyncio
from examples.test_shield import frob_a_branch
import awaitwhat


FUTURES = []


async def main():
    t = asyncio.create_task(test())
    await do_work()
    await t


async def do_work():
    loop = asyncio.get_running_loop()
    f = loop.create_future()
    FUTURES.append(f)
    branch = frob_a_branch(f)
    await asyncio.wait_for(branch, 15)


async def frob_a_branch(f):
    await f


def name(t):
    try:
        # Python3.8
        return t.get_name()
    except AttributeError:
        return f"Task-{id(t)}"


async def test():
    import sys

    await asyncio.sleep(1)
    try:
        tt = asyncio.all_tasks()
        print(awaitwhat.dot.dumps(tt))
    finally:
        for f in FUTURES:
            f.set_result(None)


if __name__ == "__main__":
    asyncio.run(main())
