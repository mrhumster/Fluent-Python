import functools
import itertools
import numbers
import operator
import math
from vector_nd import Vector


class VectorND2(Vector):
    shortcut_names = 'xyzt'

    def __len__(self):
        return len(self._components)

    def __getitem__(self, item):
        """
        >>> v7 = VectorND2(range(8))
        >>> v7[-1]
        7.0
        >>> v7[-2]
        6.0
        >>> v7[1:4]
        Vector([1.0, 2.0, 3.0])
        >>> v7[-1:]
        Vector([7.0])
        """
        cls = type(self)  # Получаем класс экземпляра
        if isinstance(item, slice):  # Если индекс - это срез, то
            return cls(self._components[item])  # вызываем класс cls для построения экземпляра Vector
        elif isinstance(item, numbers.Integral):  # абстрактный базовый класс, для гибкости ;)
            return self._components[item]  # Если индекс число, то просто возвращаем элемент
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __getattr__(self, item):
        """
        >>> v1 = VectorND2(range(10))
        >>> v1.x, v1.y, v1.z, v1.t
        (0.0, 1.0, 2.0, 3.0)
        """
        cls = type(self)
        if len(item) == 1:
            pos = cls.shortcut_names.find(item)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, item))

    def __setattr__(self, key, value):
        """
        Для исключения ошибок связанной с попыткой установить новую переменную
        из зарезервированных имен x, y, z, t

        >>> v1 = VectorND2(range(10))
        >>> v1.x = 10
        Traceback (most recent call last):
            ...
            raise AttributeError(msg)
        AttributeError: readonly attribute 'x'

        """
        cls = type(self)
        if len(key) == 1:  # если аттрибут односимвольный
            if key in cls.shortcut_names:  # и входит в переменную с именами
                error = 'readonly attribute {attr_name!r}'  # ошибка установки
            elif key.islower():
                error = 'can\'t set attributes \'a\' to \'z\' in {cls_name!r}'
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=key)
                raise AttributeError(msg)
        super().__setattr__(key, value)

    def __eq__(self, other):
        """
        Реализация оператора сравнения сделана для экономии ресурсов
        при сравнении векторов с большим количеством измерений.

        Функция zip порождает генератор кортежей, содержащих соответственно
        элементы каждого переданного итерируемого объекта.

        Сравнение длины в предыдущем предложении необходимо, потому, что
        zip без предупреждения перестает порождать значения, как только
        хотя бы один входящий аргумент будет исчерпан.

        """
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __hash__(self):
        """
        Подаем выражение hashes на вход reduce вместе с функцией xor -
        для вычисления итогового хэш-значения; третий элемент равный 0 -
        инициализатор.
        """
        hashes = map(hash, self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def angle(self, n):
        """
        Вспомогательная функция для вычисления угловой координаты.
        :param n: элементы вектора
        :return: значние угловой координаты

        >>> v1 = VectorND2(range(10))
        >>> v1.angle(2)
        1.5115267439240436
        >>> v1.angle(1)
        1.5707963267948966


        """
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        """
        Генераторное выражение для вычисления
        всех угловых координат по запросу.
        """
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        """
        Переопределю метод для возможности вывода в гиперсферических координатах.
        :param format_spec: если оканчивается на 'h': гиперсферические координаты.
        :return: Подставляет строки во внешний формат.

        >>> v1 = VectorND2(range(4))
        >>> v1.x
        0.0
        >>> v1.y
        1.0
        >>> format(v1, '.3eh')
        '<3.742e+00, 1.571e+00, 1.300e+00, 9.828e-01>'
        >>> format(v1, '.3e')
        '(0.000e+00, 1.000e+00, 2.000e+00, 3.000e+00)'
        >>> format(v1, '.3f')
        '(0.000, 1.000, 2.000, 3.000)'
        >>> format(v1, '.3fh')
        '<3.742, 1.571, 1.300, 0.983>'
        """
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            # используем itertools.chain для порождения генераторного
            # выражения, которое перебирает модуль и угловые координаты
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
