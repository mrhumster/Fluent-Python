import numbers
from vector_nd_2 import Vector2


class Vector(Vector2):
    def __mul__(self, other):
        """
        Методы для реализации умножения
        >>> v1 = Vector([1.0, 2.0, 3.0])
        >>> 14 * v1
        Vector([14.0, 28.0, 42.0])
        >>> v1 * True
        Vector([1.0, 2.0, 3.0])
        >>> from fractions import Fraction
        >>> v1 * Fraction(1, 3)
        Vector([0.3333333333333333, 0.6666666666666666, 1.0])
        """
        if isinstance(other, numbers.Real):
            return Vector(n * other for n in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        """
        Метод для реализации матричного умножения
        Для Python >= 3.5

        >>> a = Vector([1,2,3])
        >>> b = Vector([4,5,6])
        >>> a @ b
        32.0
        >>> [10, 20, 30] @ b
        320.0
        >>> a @ 1
        Traceback (most recent call last):
        ...
            File "<input>", line 1, in <module>
        TypeError: unsupported operand type(s) for @: 'Vector' and 'int'
        """
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other


if __name__ == '__main__':
    import doctest
    doctest.testmod()
