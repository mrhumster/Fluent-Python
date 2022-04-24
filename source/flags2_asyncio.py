import asyncio
import collections

import aiohttp
import tqdm
from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError
from multidict import CIMultiDict

from flags2_common import main, HTTPStatus, Result, save_flag

# По умолчанию задаем небольшое значение, что бы избежать ошибок
# на удалённом сервере, например 503 - служба временно недоступна.
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    """
    Это исключение служит лоя обертывания исключений сети и протокола
    HTTP с целью добавления к ним поля country_code, включаемого в
    сообщение об ошибке.
    """
    def __init__(self, country_code):
        self.country_code = country_code


async def get_flag(base_url, cc):
    """
    Возвращает байты загруженного изображения, либо возбуждает исключение
    web.HTTPNotFound при получении HTTP-ответа с кодом 404, либо возбуждает
    исключение aiohttp.http_exceptions.HttpProcessingError для всех остальных
    кодов состояния HTTP.
    """
    url = f'{base_url}/{cc.lower()}/{cc.lower()}.gif'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image = await response.read()
                return image
            elif response.status == 404:
                raise web.HTTPNotFound()
            else:
                raise HttpProcessingError(
                    code=response.status,
                    message=response.reason,
                    headers=CIMultiDict(response.headers)
                )


async def download_one(cc, base_url, semaphore: asyncio.Semaphore, verbose):
    """
    :param semaphore: объект класса asyncio.Semaphore, механизма
    синхронизации, ограничивающего количество одновременных запросов.
    (https://docs.python.org/3/library/asyncio-sync.html)
    """
    try:
        async with semaphore:
            # semaphore используется в качестве контекстного менеджера
            # в выражении await, чтобы не блокировать систему в целом:
            # когда счётчик семафора достигает максимально разрешенного
            # значения, блокируется только эта сопрограмма.
            image = await get_flag(base_url, cc)
            # При выходе из этого предложения with счётчик уменьшается,
            # что приводит к разблокировке объекта-сопрограммы, стоящего
            # в очереди к тому же семафору.
    except web.HTTPNotFound:
        # Если флаг не был найден, просто устанавливаем соответсвующее
        # состояние для Result.
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        # Любая другая ошибка приводит к исключению FetchError, в
        # котором хранится код страны и исходное исключение, для этого
        # используется конструкция raise X from Y, описанная в документе
        # PEP 3134 (https://peps.python.org/pep-3134/).
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower() + '.gif')
        # Эта функция записывает изображение флага на диск.
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


async def download_core(cc_list, base_url, verbose, concur_req):
    """
    Сопрограмма получает те же аргументы, что download_many, но
    вызывать ее из main напрямую нельзя, потому что это сопрограмма,
    а не обычная функция.
    """
    counter = collections.Counter()
    # Создаем объект asyncio.Semaphore, который разрешает запускать
    # одновременно не более concur_req сопрограмм.
    semaphore = asyncio.Semaphore(concur_req)
    # Создаем список объектов-сопрограмм, по одному для каждого
    # вызова сопрограммы download_one.
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]
    # Получаем итератор, который будет возвращать будущие объекты
    # по мере завершения.
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        # Обёртываем итератор функцией tqdm, что бы можно было
        # отобразить ход выполнения.
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        # Обходим завершённые будущие объекты; этот цикл очень
        # похож на цикл функции download_many. Отличия связаны
        # с обработкой исключений, что обусловлено различиями
        # в библиотеках работы с HTTP (requests и aiohttp)
        try:
            res = await future
            # Получить результаты asyncio.futures.Future проще
            # всего, воспользовавшись await вместо обращения к
            # future.results()
        except FetchError as exc:
            # Любое исключение в download_one обёртывается
            # исключением FetchError.
            country_code = exc.country_code
            # Получаем из объекта FetchError код страны, при
            # скачивании флага которой произошло исключение.
            try:
                error_msg = exc.__cause__.args[0]
                # Пытаемся извлечь сообщение об ошибке из
                # объекта исходного исключения (__cause__).
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
                # Если в исходном исключении нет сообщения об
                # ошибке, используем в этом качестве имя класса
                # исходного исключения.
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status
        counter[status] += 1
        # Подсчитываем исходы разных видов.

    # Возвращаем счётчик, как в других скриптах.
    return counter


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    coro = download_core(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    # download_many просто создаёт экземпляр сопрограммы и
    # передаёт его циклу обработки событий с помощью
    # run_until_complete.
    loop.close()
    # Когда всё сделано, завершаем цикл обработки событий
    # и возвращаем counts.
    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
