import asyncio
import signal

from awaitwhat import dot


def signal_handler(signal_number, frame):
    tt = asyncio.all_tasks()
    print(dot.dumps(tt))


def register_signal(signal_number=signal.SIGWINCH):
    signal.signal(signal_number, signal_handler)
