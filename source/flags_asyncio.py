import asyncio
import aiohttp

from flags import BASE_URL, save_flag, show, main

"""
Welcome to AIOHTTP
Asynchronous HTTP Client/Server for asyncio and Python.

Current version is 3.8.1.

https://docs.aiohttp.org/en/stable/

*** Книжка написана на Py 3.4. Учитывая современные реалии
    переписал с использование async/await синтаксиса.

1.  Все начинается с данной функции, где мы загружаем
    в цикл обработки событий несколько объектов-сопрограмм,
    полученных от download_one.

2.  Цикл обработки событий asyncio активирует все сопрограммы 
    по очереди.

3.  Когда клиентская сопрограмма, например get_flag, выполняет
    await что бы делегировать работу библиотечной сопрограмме,
    например aiohttp.request, управление возвращается циклу
    обработки событий, который может выполнять любую другую из
    ранее запланированных сопрограмм.

4.  В цикле обработки событий для получения уведомлений о 
    завершении блокирующих операций используется низкоуровневое 
    API, основанное на обратных вызовах.

5.  Когда такое случается, главный цикл отправляет результат
    приостановленной сопрограмме.
    
6.  Затем выполнение сопрограммы продолжается до следующего 
    await, например await response.read() в get_flag. Цикл 
    обработки событий вновь получает управление. Шаги 4, 5 и 6 
    повторяются до выхода из цикла обработки событий.

"""


async def get_flag(cc):
    url = f'{BASE_URL}/{cc.lower()}/{cc.lower()}.gif'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Блокирующие операции реализованы в виде сопрограмм,
            # а наш код делегирует им работу с помощью await,
            # поэтому они работают асинхронно.
            image = await response.read()
            # Чтение ответов - отдельная асинхронная операция.
            print('Status:', response.status)
    return image


async def download_one(cc):
    # download_one должна быть сопрограммой, потому что в ней
    # используется await.
    image = await get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # Создаем ссылку на внутреннюю реализацию цикла обработки событий.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Строим список объектов-генераторов, вызывая функцию download_one
    # по одному разу для каждого загружаемого изображения.
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    # Несмотря на свое имя, wait - неблокирующая функция. Это сопрограмма,
    # которая завершается, когда завершатся все переданные ей сопрограммы.
    wait_coro = asyncio.wait(to_do)
    # Выполняем цикл обработки событий, пока сопрограмма wait_coro не
    # завершится; в этом месте скрипт блокируется на все время работы цикла
    # обработки событий. Второй элемент, возвращенный функцией
    # run_until_complete, мы игнорируем.
    res, _ = loop.run_until_complete(wait_coro)

    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
