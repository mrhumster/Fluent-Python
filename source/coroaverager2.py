from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            # Что бы вернуть значение, сопрограмма должна
            # завершиться успешно, поэтому проверяется
            # условие выхода из цикла подсчета среднего
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)
