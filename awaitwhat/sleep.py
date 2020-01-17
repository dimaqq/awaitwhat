import asyncio


def mine(frame):
    return asyncio.sleep.__code__ == frame.f_code


def decode(frame):
    try:
        delay = frame.f_locals["delay"]
    except Exception:
        delay = "?"

    try:
        deadline = frame.f_locals["h"].when()
        now = frame.f_locals["future"].get_loop().time()
        remaining = deadline - now
    except Exception:
        remaining = "?"

    try:
        scheduled = frame.f_locals["h"]._scheduled
        cancelled = frame.f_locals["h"]._cancelled
        state = (
            "cancelled" if cancelled else "scheduled" if scheduled else "not started"
        )
    except Exception:
        state = "?"

    return f"asyncio.sleep: state {state} delay {delay} remaining {remaining}"
