import math
import reprlib
from array import array


class Vector:
    typecode = 'd'

    def __init__(self, components):
        """
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
        >>> v1 = Vector((1, 2, 3, 4, 5))
        >>> repr(v1)
        'Vector([1.0, 2.0, 3.0, 4.0, 5.0])'
        """
        components = reprlib.repr(self._components)
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
        >>> v1 = Vector([1,1])
        >>> bytes(v1)
        b'd\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?'
        """
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        """
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