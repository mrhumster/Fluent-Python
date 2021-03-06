import math
from array import array


class Vector2d:
    """
    :typecode: -- аттрибут класса для преобразования
    экземпляра Vector2d последовательность байтов и обратно.

    >>> v1 = Vector2d(3, 4)
    >>> print(v1.x, v1.y)
    3.0 4.0
    >>> x, y = v1
    >>> x, y
    (3.0, 4.0)
    >>> v1
    Vector2d(3.0, 4.0)
    >>> v1_clone = eval(repr(v1))
    >>> v1 == v1_clone
    True
    >>> print(v1)
    (3.0, 4.0)
    >>> octets = bytes(v1)
    >>> abs(v1)
    5.0
    >>> bool(v1), bool(Vector2d(0, 0))
    (True, False)
    """
    typecode = 'd'

    def __init__(self, x, y):
        """
        Преобразование x, y в тип float в методе инициализации
        позволяет на ранней стадии обнаруживать ошибки. Это
        полезно когда конструктор вызывается с не подходящими
        аргументами
        """
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        """
        Наличие __iter__ делает объект итерируемым.
        Благодаря ему работает распаковка (пр.: x, y = ny_vector).
        В данном случае реализация при помощи генераторного
        выражения, который отдает компоненты поочередно.
        """
        return (i for i in (self.x, self.y))

    def __repr__(self):
        """
        Метод __repr__ строит строку, интерполируя компоненты с
        помощью синтаксиса {!r} для получения их представления,
        возвращаемого функцией repr; Поскольку Vector2d - итерируемый
        объект, *self поставляет компоненты x и y функции format.
        """
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(class_name, *self)

    def __str__(self):
        """
        Из итерируемого объекта легко построить кортеж для отображения
        в виде упорядоченной пары.
        """
        return str(tuple(self))

    def __bytes__(self):
        """
        Для генерации объекта типа bytes мы преобразуем typecode
        в bytes и конкатенируем с объектом bytes, полученным
        преобразованием массива, который построен путём обхода
        экземпляра.
        """
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        """
        Для быстрого сравнения всех компонентов мы строим кортеж
        их операндов. Это работает, когда операнды являются экземплярами
        класса Vector2d, но не без проблем.
        """
        return tuple(self) == tuple(other)

    def __abs__(self):
        """
        Модулем вектора называется длина гипотенузы прямоугольного
        треугольника, где катеты x и y.
        """
        return math.hypot(self.x, self.y)

    def __bool__(self):
        """
        Метод __bool__ вызывает abs(self) для вычисления модуля, а
        затем преобразует полученное значение в тип bool, так что
        0.0 преобразуется в False, а любое отличное от нуля в True
        """
        return bool(abs(self))

    def __format__(self, format_spec=''):
        """
        :param format_spec: применяется к каждому компоненту вектора
        с помощью встроенной функцией format и строит итерируемый объект,
        порождающий отформатированные строки.
        :return: Подставляем отформатированные строки в шаблон (x, y).
        """
        components = (format(c, format_spec) for c in self)
        return '({}, {})'.format(*components)

if __name__ == "__main__":
    import doctest
    doctest.testmod()