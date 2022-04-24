import asyncio
import sys

from aiohttp import web


from charfinder import UnicodeNameIndex
# Конструктор UnicodeNameIndex читает индекс из файла
# charfinder_index.pickle, если такой существует, в
# противном случае строит индекс, поэтому ответ на
# первый запрос может занять на несколько секунд
# больше времени.
index = UnicodeNameIndex()

TEMPLATE_NAME = 'http_charfinder.html'
CONTENT_TYPE = 'text/html'
SAMPLE_WORDS = 'bismillah chess cat circled Malayalam digit'.split()

ROW_TPL = '<tr><td>{code_str}</td><th>{char}</th><td>{name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in sorted(SAMPLE_WORDS, key=str.upper))

with open(TEMPLATE_NAME) as tpl:
    template = tpl.read()

template = template.replace('{links}', LINKS_HTML)


def home(request):
    """
    :param request: экземпляр aiohttp.web.Request
    :return: экземпляр aiohttp.web.Response
    """
    # Получаем строку запроса, из которой удалены начальные и конечные пробелы.
    query = request.query.get('query', '').strip()
    # Протоколируем запрос на консоли сервера.
    print(f'Query: {query!r}')
    # Если запрос был, то связываем res со строками HTML-таблицы, построенной
    # по результатам запроса к индексу, а msg - с сообщением о состоянии.
    if query:
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**descr._asdict()) for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    # Отрисовываем html-страницу.
    html = template.format(query=query, result=res, message=msg)
    # Протоколируем ответ на консоли сервера.
    print(f'Sending {len(descriptions)} results')
    # Строим и возвращаем объект Response.
    return web.Response(content_type=CONTENT_TYPE, charset='UTF-8', text=html)


async def init(loop, address, port):
    """
    Сопрограмма отдает сервер, который будет
    обрабатывать запросы в цикле обработки событий.
    """
    # Класс aiohttp.web.Application предоставляет веб-приложение...
    app = web.Application(loop=loop)
    # ... в котором маршруты сопоставляют функции-обработчики
    # образцам URL-адресов; в данном случае запрос GET /
    # маршрутизируется функции home
    app.router.add_route('GET', '/', home)
    # Метод app.make_handler возвращает объект типа
    # aiohttp.web.RequestHandler, который обрабатывает
    # HTTP-запросы в соответствии с маршрутами, заданными в app.
    handler = app.make_handler()
    # Метод create_server создает сервер, использующий в качестве
    # обработчика протокола объект handler, и связывает его с
    # адресом address и портом port.
    server = await loop.create_server(handler, address, port)
    # Возвращаем адрес и порт первого сокета сервера.
    return server.sockets[0].getsockname()


def main(address='127.0.0.1', port=8888):
    port = int(port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Вызываем init для запуска сервера и получения его адреса и порта.
    host = loop.run_until_complete(init(loop, address, port))
    print(f'Serving on {host}. Hit CTRL-C to stop.')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print('Server shutting down.')
    loop.close()


if __name__ == '__main__':
    main(*sys.argv[1:])
