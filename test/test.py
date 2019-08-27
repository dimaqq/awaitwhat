import asyncio
import linecache
from awaitwhat import extended_stack


def trace_all_tasks():
    print("#### Python built-in stack trace")
    for t in asyncio.Task.all_tasks():
        print("---- task")
        for frame in t.get_stack():
            print(frame)
        print()


def extended_trace_all_tasks():
    print("#### Extended stack trace")
    extracted_list = []
    checked = set()
    for t in asyncio.Task.all_tasks():
        print("---- task")
        for f in extended_stack(t.get_stack()):
            try:
                # borrowed from cpython/Lib/asyncio/base_tasks.py
                lineno = f.f_lineno
                co = f.f_code
                filename = co.co_filename
                name = co.co_name
                if filename not in checked:
                    checked.add(filename)
                    linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                extracted_list.append((filename, lineno, name, line))
                print(filename, lineno, line)
            except Exception as e:
                print(f, e)
        print()
    return extracted_list

    # FIXME
    exc = task._exception
    if not extracted_list:
        print(f"No stack for {task!r}", file=file)
    elif exc is not None:
        print(f"Traceback for {task!r} (most recent call last):", file=file)
    else:
        print(f"Stack for {task!r} (most recent call last):", file=file)

    traceback.print_list(extracted_list, file=file)
    if exc is not None:
        for line in traceback.format_exception_only(exc.__class__, exc):
            print(line, file=file, end="")


async def tester():
    await asyncio.sleep(0.1)
    trace_all_tasks()
    extended_trace_all_tasks()


async def job():
    await foo()


async def foo():
    await bar()


async def bar():
    await baz()


async def baz():
    await leaf()


async def leaf():
    await asyncio.sleep(1)


async def work():
    await asyncio.gather(tester(), job())


asyncio.run(work())


# TODO
#
# When a coro is blocked on gather(), the thing on the stack is:
# <_asyncio.FutureIter object at 0x1086b1040>
#
# This is because instruction preceding YIELD_FROM is GET_AWAITABLE
# Which converts Future into an iterator:
#
# https://github.com/python/cpython/blob/51aac15f6d525595e200e3580409c4b8656e8a96/Modules/_asynciomodule.c#L1633
