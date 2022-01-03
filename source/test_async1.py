import asyncio


async def gather_fxn1():
    print('6 start')
    await asyncio.sleep(6)
    print('6 end')


async def gather_fxn2():
    print('4 start')
    await asyncio.sleep(4)
    print('4 end')


async def sample_coroutine():
    await asyncio.gather(gather_fxn1(), gather_fxn2())

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(sample_coroutine())