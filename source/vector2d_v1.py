import math

from source.vector2d_v0 import Vector2d


class Vector2dv1(Vector2d):
    def __init__(self, x, y):
        super().__init__(x, y)

    @classmethod
    def from_bytes(cls, octets):
        """
            Метод класса снабжён декоратором classmethod
            Аргумент self отсутствует; вместо него в аргументе
            cls передается сам класс.
        """
        typecode = chr(octets[0])   # Читаем typecode из первого байта
        memv = memoryview(octets[1:]).cast(typecode)
        """
            Создаем объект memoryview из двоичной последовательности
            октетов и приводим его к типу typecode
            Распаковываем memoryview, получившийся в результате приведения
            типа, и получаем пару аргументов, необходимых конструктору
        """
        return cls(*memv)

    def angle(self):
        """
        Данный метод для получения угла.
        :return: atg
        """
        return math.atan2(self.y, self.x)

    def __format__(self, format_spec=''):
        """
        Переопределю метод для возможности вывода в полярных координатах.
        :param format_spec: если оканчивается на 'p': полярные координаты.
        :return: Подставляет строки во внешний формат.
        """
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(*components)
