import math
import reprlib
from array import array


class Vector:
    typecode = 'd'

    def __init__(self, components):
        """
        В "защищённом" атрибуте экземпляра self._comoponents
        хранится массив array компонент Vector

        >>> Vector([3.1, 4.2])
        Vector([3.1, 4.2])
        >>> Vector((3, 4, 5))
        Vector([3.0, 4.0, 5.0])
        >>> Vector(range(10))
        Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
        """
        self._components = array(self.typecode, components)

    def __iter__(self):
        """
        Что бы была возможность иттерировать объект
        возвращаем иттератор основаный на _components

        >>> for i in Vector([1, 2, 3, 4]):
        ...     print(i)
        ...
        1.0
        2.0
        3.0
        4.0
        """
        return iter(self._components)

    def __repr__(self):
        """
        Используем reprlib.repr() для получения представления
        self._components ограниченной длины

        >>> v1 = Vector((1, 2, 3, 4, 5))
        >>> repr(v1)
        'Vector([1.0, 2.0, 3.0, 4.0, 5.0])'
        >>> v1 = Vector([1, 2, 3, 4, 5, 6, 7, 8])
        >>> repr(v1)
        'Vector([1.0, 2.0, 3.0, 4.0, 5.0, ...])'
        """
        components = reprlib.repr(self._components)
        # Удаляем префикс array('d' и закрываем скобку ),
        # перед тем как подставить строку в вызов конструктора.
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        """
        >>> v1 = Vector((1, 2, 3, 4, 5))
        >>> str(v1)
        '(1.0, 2.0, 3.0, 4.0, 5.0)'
        """
        return str(tuple(self))

    def __bytes__(self):
        """
        Строим объект bytes из self._components

        >>> v1 = Vector([1,1])
        >>> bytes(v1)
        b'd\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?'
        """
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        """
        Метод hypot больше не применим, поэтому
        вычисляем сумму квадратов компонент и извлекаем
        из неё квадратный корень.

        >>> v1 = Vector([3, 4])
        >>> abs(v1)
        5.0
        """
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        """
        >>> bool(Vector([0, 0]))
        False
        >>> bool(Vector([1, 1]))
        True
        """
        return bool(abs(self))

    @classmethod
    def from_bytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
