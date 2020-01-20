import asyncio
import awaitwhat.wait
import awaitwhat.blocker
from awaitwhat.stack import task_get_stack


async def a():
    await asyncio.wait(b(), timeout=123)


async def b():
    await asyncio.sleep(42)


async def debug():
    t = asyncio.create_task(a())
    await asyncio.sleep(0.11)
    stack = task_get_stack(t, None)
    return stack


def test_wait():
    async def test():
        t = asyncio.create_task(a())
        try:
            await asyncio.sleep(0.11)

            stack = task_get_stack(t, None)
            assert awaitwhat.wait.mine(stack[-2])
            text = awaitwhat.wait.decode(stack[-2])
            assert "asyncio.wait" in text
            assert "scheduled" in text
            assert "delay 42" in text
            assert "remaining 41.8" in text
        finally:
            t.cancel()

    return asyncio.run(test())


def test_blockers():
    async def test():
        t = asyncio.create_task(a())
        try:
            await asyncio.sleep(0.11)

            text = awaitwhat.blocker.blockers(t)
            assert "asyncio.wait" in text
            assert "scheduled" in text
            assert "delay 42" in text
            assert "remaining 41.8" in text
        finally:
            t.cancel()

    asyncio.run(test())
