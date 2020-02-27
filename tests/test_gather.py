import asyncio
import awaitwhat.blocker
from awaitwhat.stack import task_get_stack


async def a():
    await asyncio.gather(asyncio.sleep(0.01), asyncio.sleep(999 + 1))


def fixme_dont_test_sleep():
    async def test():
        t = asyncio.create_task(a())
        try:
            await asyncio.sleep(0.11)

            stack = task_get_stack(t, None)
            # assert awaitwhat.sleep.mine(stack[-2])
            # text = awaitwhat.sleep.decode(stack[-2])
            # assert "asyncio.sleep" in text
            # assert "scheduled" in text
            # assert "delay 42" in text
            # assert "remaining 41.8" in text
        finally:
            t.cancel()

    asyncio.run(test())


def test_blockers():
    async def test():
        t = asyncio.create_task(a())
        try:
            await asyncio.sleep(0.11)

            text = str(awaitwhat.blocker.blockers(t))
            assert "Task finished" in text
            assert "Task pending" in text
        finally:
            t.cancel()

    asyncio.run(test())
