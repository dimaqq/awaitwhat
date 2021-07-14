import asyncio


def mine(frame):
    return asyncio.wait_for.__code__ == frame.f_code


def decode(frame):
    try:
        timeout = frame.f_locals["timeout"]
    except Exception:
        timeout = "?"
    try:
        timeout_handle_deadline = frame.f_locals["timeout_handle"].when()
        now = frame.f_locals["waiter"].get_loop().time()
        timeout_remaining = timeout_handle_deadline - now
    except Exception:
        timeout_remaining = "?"
    try:
        awaitable = frame.f_locals["fut"]
    except Exception:
        awaitable = None
    return [
        f"asyncio.wait_for: timeout {timeout} remaining {timeout_remaining}",
        awaitable,
    ]
