import asyncio

import aiohttp
from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError
from multidict import CIMultiDict

from flags2_asyncio import download_many, download_core, FetchError
from source.flags2_common import HTTPStatus, save_flag, Result


async def http_get(url):
    """
    Общий код для скачивания файла из Интернета.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                ctypes = response.headers.get('Content-type', '').lower()
                if 'json' in ctypes or url.endswith('json'):
                    # Если тип содержимого содержит подстроку 'json' или
                    # аргумент url заканчивается строкой .json, то разбираем
                    # ответ методом response.json() и возвращаем структуру
                    # данных Python - в данном случае словарь dict.
                    data = await response.json()
                else:
                    # В противном случае просто читаем поступающие байты.
                    data = await response.read()
                return data
            elif response.status == 404:
                raise web.HTTPNotFound()
            else:
                raise HttpProcessingError(
                    code=response.status,
                    message=response.reason,
                    headers=CIMultiDict(response.headers))


async def get_country(base_url, cc):
    """
    Эта сопрограмма скачивает файл metadata.json,
    соответствующий коду стран, и получает из него
    название страны.
    """
    url = f'{base_url}/{cc.lower()}/metadata.json'
    # В metadata записывается словарь Python,
    # построенный в результате разбора содержимого
    # в формате JSON.
    metadata = await http_get(url)
    return metadata['country']


async def get_flag(base_url, cc):
    """
    Большая часть кода перенесена из этой сопрограммы
    в новую сопрограмму http_get, чтобы этим кодом
    можно было воспользоваться и в get_country.
    """
    url = f'{base_url}/{cc.lower()}/{cc.lower()}.gif'
    return await http_get(url)


async def download_one(cc, base_url, semaphore, verbose):
    """
    Теперь в этой сопрограмме используется
    await для делегирования работы сопрограмм
    get_flag и get_country.
    """
    try:
        # Я поместил вызовы get_flag и get_country
        # в разные блоки with, управляемые семафором,
        # потому что не хочу удерживать семафор дольше,
        # чем необходимо.
        with await semaphore:
            image = await get_flag(base_url, cc)
        with await semaphore:
            country = await get_country(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        country = country.replace(' ', '_')
        filename = f'{country}-{cc}.gif'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_in_executor(None, save_flag, image, filename)
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)
