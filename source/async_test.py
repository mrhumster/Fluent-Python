import asyncio


async def sample_coroutine():   # Образец программы
    print('5 start')
    await asyncio.sleep(5)
    print('5 end')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(sample_coroutine())

