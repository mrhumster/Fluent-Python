from coroutil import coroutine


@coroutine
def averager():
    """
    A coroutine to compute a running average
    Сопрограмма для вычисления текущего среднего значения

    >>> coro_avg = averager()   # вызываем `averager()`, она создает объект-генератор, который
    >>> from inspect import getgeneratorstate   # инициализируется в функции `primer` декоратора `coroutine`
    >>> getgeneratorstate(coro_avg) # возвращает `'GEN_SUSPENDED'`, т.е. программа готова к приему значений
    'GEN_SUSPENDED'
    >>> coro_avg.send(10)   # мы можем сразу отправлять значения, в этом и состоял смысл генератора
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0
    """
    total = .0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count


if __name__ == '__main__':
    import doctest
    doctest.testmod()