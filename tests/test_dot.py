import asyncio
import awaitwhat
import sys

def test_stack():
    FUTURES = []


    async def main():
        t = asyncio.create_task(test())
        await do_work()
        await t


    async def do_work():
        futs = [frob_a_tree() for i in range(1)]
        await asyncio.gather(*futs)


    async def frob_a_tree():
        await b_tree()


    async def b_tree():
        f = asyncio.Future()
        FUTURES.append(f)
        await asyncio.shield(frob_a_branch(f))


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
        # print("### Python native")
        # for t in asyncio.all_tasks():
        # print(name(t))
        # asyncio.base_tasks._task_print_stack(t, None, sys.stdout)
        # print()

        # Extended stack
        # import awaitwhat

        try:
            tt = asyncio.all_tasks()
            print(awaitwhat.dot.dumps(tt))
        finally:
            for f in FUTURES:
                f.set_result(None)


    asyncio.run(main())
