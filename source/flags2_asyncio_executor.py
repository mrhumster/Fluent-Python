import asyncio

from aiohttp import web

from source.flags2_asyncio import FetchError
from source.flags2_common import HTTPStatus, save_flag, Result
from source.flags_asyncio import get_flag


async def download_one(cc, base_url, semaphore: asyncio.Semaphore, verbose):
    try:
        async with semaphore:
            image = await get_flag(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        # Получаем ссылку на объект, представляющий цикл обработки событий.
        loop = asyncio.get_event_loop()
        # Первый аргумент run_in_executor - экземпляр исполнителя; если он
        # равен None, то используется исполнитель по умолчанию, основанный
        # на пуле потоков. Остальные аргументы - вызываемый объект и его
        # позиционные аргументы.
        loop.run_in_executor(None, save_flag, image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)