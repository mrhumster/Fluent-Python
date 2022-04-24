"""
Коротко: мы подключаемся к веб-сокету, указанному конкретным URL.
Каждое сообщение, созданное сервером веб-сокета, логируется.

async/await — это просто специальный синтаксис для комфортной
работы с промисами. Промис — не более чем объект, представляющий
собой возможную передачу или сбой асинхронной операции.
"""

import websockets
import asyncio
import logging


logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: websockets.WebSocketClientProtocol) -> None:
    async for message in websocket:
        # async for — это что-то вроде синхронного цикла for, позволяющего асинхронное
        # восприятие. Асинхронный IO позволяет выполнять перебор асинхронного итератора:
        # вы можете вызывать асинхронный код на любом этапе перебора, в то время как
        # обычный цикл for этого не позволяет.
        log_message(message)


async def consume(hostname: str, port: int) -> None:
    # consume - потребитель
    # URL ресурса веб-сокета использует собственную схему,
    # начинающуюся с ws (или wss для безопасного подключения).
    websocket_resource_url = f'ws://{hostname}:{port}'
    # Открываем соединение с веб-сокетом, используя websockets.connect:
    async with websockets.connect(websocket_resource_url) as websocket:
        # Ожидание соединения вызывает WebSocketClientProtocol, который
        # затем используется для отправки и получения сообщений.
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f'Message: {message}')


if __name__ == '__main__':
    # Этот пример кода будет принимать сообщения от ws://localhost:4000.
    # Если сервер не запущен, он выдаст ошибку 404 Not Found.
    asyncio.run(consume(hostname='localhost', port=4000))
