import asyncio
import awaitwhat
import signal


async def main():
    await job()


async def job():
    await foo()


async def foo():
    signal.alarm(1)
    await asyncio.sleep(1)


if __name__ == "__main__":
    awaitwhat.helpers.register_signal(signal.SIGALRM)
    asyncio.run(main())
