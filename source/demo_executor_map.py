from concurrent import futures
from time import strftime, sleep


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    """
    loiter - (анг.) бездельничать.
    """
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10


def main():
    display('Script starting')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    # Создаём ThreadPool с тремя потоками.
    results = executor.map(loiter, range(5))
    # Передаём исполнителю пять задач (поскольку есть
    # только три потока, сразу начнут выполнение лишь
    # три из них); это не блокирующий вызов.
    display('results:', results)
    # Немедленно распечатываем объект results,
    # полученный от executor.map: это генератор.
    display('Waiting for individual results:')
    # Обращение к enumerate в цикле for неявно вызывает
    # функцию next(results), которая, в свою очередь
    # вызывает метод _f.result() (внутреннего) будущего
    # объекта _f, представляющего первый вызов, loiter(0).
    for i, result in enumerate(results):
        # Метод result блокирует программу до завершения
        # будущего объекта, поэтому каждая итерация этого
        # цикла будет ждать готовности следующего результата.
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
