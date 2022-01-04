from source.vector2d_v1 import Vector2dv1


class Vector(Vector2dv1):
    __slots__ = ('__x', '__y')
    """
    Реализация класса Vector с не изменяемыми атрибутами
    """
    def __init__(self, x, y):
        """
        Используем __ что бы сделать атрибуты закрытыми
        """
        self.__x = float(x)
        self.__y = float(y)

    @property   # Определяет метод чтения свойств
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)