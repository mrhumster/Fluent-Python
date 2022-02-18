from datetime import date, datetime, time
from functools import singledispatchmethod


class Formatter:
    """
    Пример использования декоратора для диспетчеризациия
    функций в зависимости от типа аргумента

    https://martinheinz.dev/blog/50
    """
    @singledispatchmethod
    def format(self, args):
        raise NotImplementedError(f'Can not format value of type {type(args)}')

    @format.register
    def _(self, args: date):
        return args.strftime('%d/%m/%Y')

    @format.register
    def _(self, args: datetime):
        return args.strftime('%d/%m/%Y %H:%M:%S')

    @format.register
    def _(self, args: time):
        return args.strftime('%H:%M:%S')

    def __call__(self, args):
        return self.format(args)


if __name__ == '__main__':
    f = Formatter()
    samples = (date(2021, 2, 14), time(12, 59, 50), datetime(2021, 2, 14, 12, 59, 50))
    print(list(f(sample) for sample in samples))
