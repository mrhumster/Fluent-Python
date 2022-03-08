from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    """
    Субгенератор
    """
    total = .0
    count = 0
    average = None
    while True:
        term = yield
        # каждое значение, отправленное клиентским
        # кодом, здесь связывается с переменной term.
        if term is None:
            # Условие окончания. Без него выражение
            # yield from, вызвавшее эту сопрограмму,
            # оказалось бы навечно заблокированным.
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)
    # Возвращённое значение Result является значением
    # выражения yield from в grouper


def grouper(results, key):
    """
    Делегирующий генератор
    """
    while True:
        # На каждой итерации этого цикла создается
        # новый экземпляр averager; каждый из них
        # является объектом-генератором, работающим
        # как сопрограмма.
        # Значение, отправленное генератору grouper,
        # помещается выражением yield from в канал,
        # открытый с объектом averager.
        # grouper остается остановленным, пока averager
        # потребляет значения, отправляемые клиентом.
        # Когда выполнение averager завершится,
        # возвращённое им значение будет связано с
        # result[key].
        # После этого в цикле white создается очередной
        # экземпляр averager для потребления последующих
        # значений.
        results[key] = yield from averager()


def main(data):
    """
    Клиентский код или вызывающая сторона в терминологии
    PEP 380. Эта функция управляет всеми остальными
    """
    results = {}
    for key, values in data.items():
        group = grouper(results, key)   # <- Делегирующий генератор
        # group -- объект-генератор, получающийся в результате
        # вызова grouper с аргументом results -- словарём, в
        # котором будут собираться результаты, - и key - конкретным
        # ключом этого словаря. Этот объект будет работать как
        # сопрограмма.
        next(group)
        # Инициализируем сопрограмму
        for value in values:
            group.send(value)
            # Отправляем каждое значение value объекту grouper.
            # Оно будет получено в строке term = yield кода averager;
            # grouper его никогда не увидит.
        group.send(None)
        # Отправка значения None объекту grouper приводит к завершению
        # текущего экземпляра averager и дает возможность grouper
        # возобновить выполнение и создать очередной объект averager
        # для обработки следующей группы значений.
    # print(results)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print(f'{result.count:2} {group:5} averaging {result.average:.2f}{unit}')


data = {
    'girls;kg': [40.9, 44.4, 40.9, 44.4, 40.9, 44.4, 40.9, 44.4, ],
    'girls;m': [1.6, 1.72, 1.5, 1.6, 1.72, 1.5, 1.6, 1.72, 1.5, ],
    'boys;kg': [40.9, 44.4, 40.9, 44.4, 40.9, 44.4, 40.9, 44.4, ],
    'boys;m': [1.6, 1.72, 1.5, 1.6, 1.72, 1.5, 1.6, 1.72, 1.5, ],
}

if __name__ == '__main__':
    main(data)