import types
from . import _what


def extended_stack(s):
    stack = s[:]
    while isinstance(stack[-1], types.FrameType):
        try:
            n = _what.next(stack[-1])
        except Exception as e:
            n = str(e)
        try:
            f = n.cr_frame
        except Exception as e:
            f = f"{n}: {e}"
        stack.append(f)
    return stack


def frames(coro):
    """To be removed"""
    while coro:
        try:
            yield f"{coro.__name__} ip {coro.cr_frame.f_lasti}"
        except Exception as e:
            yield str(coro)
            return

        try:
            coro = _what.next(coro.cr_frame)
        except Exception as e:
            yield str(e)
            return


def foretrace(coro):
    """To be removed"""
    for line in frames(coro):
        print(line)
    print()
