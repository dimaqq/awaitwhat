import asyncio
import awaitwhat


global_futures = list() # Structure to hold a global future

async def main():
    # generate a global future
    global_futures.append(asyncio.Future())
    t = asyncio.create_task(test())
    await do_work()
    await t


async def do_work():
    futs = [frob_a_tree() for i in range(3)]
    await asyncio.gather(*futs)


async def frob_a_tree():
    await b_tree()


async def b_tree():
    # Create a task with a global future
    ff = global_futures[-1]
    t = asyncio.create_task(frob_a_branch(ff))
    await asyncio.gather(t)


async def frob_a_branch(f):
    await b_branch(f)


async def b_branch(f):
    await f


def name(t):
    try:
        # Python3.8
        return t.get_name()
    except AttributeError:
        return f"Task-{id(t)}"


async def test():
    import sys

    await asyncio.sleep(0.1)

    try:
        tt = asyncio.all_tasks()
        print(awaitwhat.dot.dumps(tt))
    finally:
        global_futures[-1].set_result(None)


if __name__ == "__main__":
    asyncio.run(main())
