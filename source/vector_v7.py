import numbers
from vector_nd_2 import Vector2


class Vector(Vector2):
    """
    >>> v1 = Vector([1.0, 2.0, 3.0])
    >>> 14 * v1
    Vector([14.0, 28.0, 42.0])
    >>> v1 * True
    Vector([1.0, 2.0, 3.0])
    >>> from fractions import Fraction
    >>> v1 * Fraction(1, 3)
    Vector([0.3333333333333333, 0.6666666666666666, 1.0])
    """

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return Vector(n * other for n in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other


if __name__ == '__main__':
    import doctest
    doctest.testmod()
