import asyncio
import awaitwhat

SECRET = 1.2345


async def sleeper():
    await asyncio.sleep(SECRET)


async def job():
    await sleeper()


async def main():
    t = asyncio.create_task(job())
    await asyncio.sleep(0.1)
    print(awaitwhat.dot.dumps(asyncio.all_tasks()))


if __name__ == "__main__":
    asyncio.run(main())
