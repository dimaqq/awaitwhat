# Await, What?

Tell you what waits for what in an `async/await` program.

#### Mailing list reference

https://mail.python.org/archives/list/async-sig@python.org/thread/6E2LRVLKYSMGEAZ7OYOYR3PMZUUYSS3K/


#### Original post dump

Hi group,

I'm recently debugging a long-running asyncio program that appears to
get stuck about once a week.

The tools I've discovered so far are:
high level: `asyncio.all_tasks()` + `asyncio.Task.get_stack()`
low level: `loop._selector._fd_to_key`

What's missing is the middle level, i.e. stack-like linkage of what is
waiting for what. For a practical example, consider:

async def leaf(): await somesocket.recv()
async def baz(): await leaf()
async def bar(): await baz()
async def foo(): await bar()
async def job(): await foo()
async def work(): await asyncio.gather(..., job())
async def main(): asyncio.run(work())

The task stack will contain:
* main and body of work with line number
* job task with line number pointing to foo
The file descriptor mapping, docket fd, loop._recv() and a Future.

What's missing are connections foo->bar->baz->leaf.
That is, I can't tell which task is waiting for what terminal Future.

Is this problem solved in some way that I'm not aware of?
Is there a library or external tool for this already?

Perhaps, if I could get a list of all pending coroutines, I could
figure out what's wrong.

If no such API exists, I'm thinking of the following:

async def foo():
    await bar()

In [37]: dis.dis(foo)
  1           0 LOAD_GLOBAL              0 (bar)
              2 CALL_FUNCTION            0
              4 GET_AWAITABLE
              6 LOAD_CONST               0 (None)
              8 YIELD_FROM
             10 POP_TOP
             12 LOAD_CONST               0 (None)
             14 RETURN_VALUE

Starting from a pending task, I'd get it's coroutine and:
get the coroutine frame, and if current instruction is YIELD_FROM,
then the reference to the awaitable should be on the top of the stack.
If that reference points to a pending coroutine, I'd add that to the
"forward trace" and repeat.
at some point I'd reach an awaitable that's not a pending coroutine,
which may be: another Task (I already got those), a low-level Future
(can be looked up in event loop), an Event (tough luck, shoulda logged
all Events on creation) or a dozen other corner cases.

What do y'all think of this approach?

Thanks,
D.
