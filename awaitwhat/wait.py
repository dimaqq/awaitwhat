import asyncio.tasks


def mine(frame):
    return asyncio.tasks._wait.__code__ == frame.f_code


def decode(frame):
    pass
