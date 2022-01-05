from vector_nd import Vector


class Vector2(Vector):
    def __len__(self):
        """
        >>> v1 = Vector2([3, 4, 5])
        >>> len(v1)
        3
        """
        return len(self._components)

    def __getitem__(self, item):
        """
        В данной реализации есть проблема. Срез будет
        объектом класс list. Было бы лучше, если срез
        был бы объектом класса Vector.

        >>> v1 = Vector2([3, 4, 5])
        >>> v1[0], v1[-1]
        (3.0, 5.0)
        >>> v7 = Vector2(range(7))
        >>> v7[1:4]
        array('d', [1.0, 2.0, 3.0])
        """
        return self._components[item]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
