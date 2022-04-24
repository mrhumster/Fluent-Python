# Класс UnicodeNameIndex отвечает за построение
# индекса имён и представляет методы запроса.
import asyncio
import sys

from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '

# Конструктор UnicodeNameIndex читает индекс из файла
# charfinder_index.pickle, если такой существует, в
# противном случае строит индекс, поэтому ответ на
# первый запрос может занять на несколько секунд
# больше времени.
index = UnicodeNameIndex()


async def handle_queries(reader, writer):
    """
    Это сопрограмма, которую мы должны передать методу
    asyncio.start_server; её аргументами являются
    asyncio.StreamReader и asyncio.StreamWriter.
    :param reader:
    :param writer:
    :return:
    """
    while True:
        # В этом цикле обрабатывается сеанс, который
        # продолжается до получения любого управляющего
        # символа от клиента.
        writer.write(PROMPT)
        # Метод StreamWriter.write - не сопрограмма, а
        # обычная функция; в этой строке выводится
        # приглашение ?>.
        await writer.drain()
        # Метод StreamWriter.drain сбрасывает буфер записи;
        # это сопрограмма, поэтому вызывать через await.
        data = await reader.readline()
        # Метод reader.readline - сопрограмма, он возвращает
        # объект типа bytes
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            # Это исключение может возникнуть, если клиент Telnet посылает
            # управляющий символ; в таком случае мы для простоты считаем,
            # что получен нулевой символ.
            query = '\x00'
        client = writer.get_extra_info('peername')
        # Здесь возвращается удалённый адрес сокета.
        print(f'Received from {client}: {query}')
        if query:
            if query == 'exit()':
                # Выходим, если получен команда на выход.
                break
            lines = list(index.find_description_strs(query))
            # Возвращаем генератор, который отдаёт строки, содержащие
            # кодовую позицию Unicode, сам символ и его имя; для простоты
            # создаю из генератора список.
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
                # Отправляем клиенту строки, преобразованные в последовательность
                # байтов в предположении кодировки UTF-8, в конце каждой строки добавляем
                # символы возврата каретки и перевода строки; обратите внимание, что
                # аргумент - генераторное выражение.
            writer.write(index.status(query, len(lines)).encode() + CRLF)
            # Выводим строку состояния.

            await writer.drain()
            # Сбрасываем буфер вывода.
            print(f'Sent {len(lines)} results')
            # Протоколируем ответ на консоли сервера.
    print('Close the client socket')
    # Протоколируем конец сеанса на консоли сервера.
    writer.close()
    # Закрываем StreamWriter.


def main(address='127.0.0.1', port=2323):
    """
    Функцию main можно запускать без аргументов.
    :param address: адрес TCP сервера
    :param port: порт TCP сервера
    """
    port = int(port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_coro = asyncio.start_server(handle_queries, address, port)
    # По завершении объект-сопрограмма, полученный от asyncio.start_server,
    # возвращает экземпляр asyncio.Server, TCP-сервера.
    server = loop.run_until_complete(server_coro)
    # Управляя сопрограммой server_coro? получаем объект server.
    host = server.sockets[0].getsockname()
    # Получаем адрес и порт первого сокета сервера и выводим его в терминал.
    print(f'Serving on {host}. Hit Ctrl+C to stop.')
    try:
        # Исполняем цикл обработки событий; здесь функция main блокируется
        # до тех пор, пока на консоли сервера не будет нажата CTRL+C.
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Server shutting down.')
    server.close()
    # Метод server.wait_closed() возвращает будущий объект; дадим ему
    # возможность выполнить свою работу с помощью метода loop.run_until_complete.
    loop.run_until_complete(server.wait_closed())
    # Завершаем цикл обработки событий.
    loop.close()


if __name__ == '__main__':
    # Это краткий способ выразить обработку необязательных аргументов командной
    # строки: разворачиваем sys.argv[1:] и передаём результат функции main, в
    # которой заданы также значения аргументов по умолчанию.
    main(*sys.argv[1:])
