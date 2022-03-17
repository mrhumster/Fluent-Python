import asyncio
import itertools
import sys


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    status = ''
    for char in itertools.cycle(('...', 'o..', 'Oo.', 'oOo', '.oO', '..o')):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    await asyncio.sleep(10)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin('thinking!'))
    print('spinner object:', spinner)
    result = await slow_function()
    spinner.cancel()
    return result


async def main():
    result = await supervisor()
    print('Answer:  ', result)


if __name__ == '__main__':
    asyncio.run(main())
