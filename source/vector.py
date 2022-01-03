from math import hypot


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        """
        Строковое представление объекта
        """
        return f'Vector({self.x}, {self.y})'

    def __abs__(self):
        """
        :return: Return the absolute value of obj.
        """
        return hypot(self.x, self.y)

    def __bool__(self):
        """
        Вызывается для реализации проверки истинности и встроенной операции bool();
        должен вернуть False или True. Когда этот метод не определен, вызывается __len __(),
        если он определен, и объект считается истинным, если его результат не равен нулю.
        Если класс не определяет ни __len__(), ни __bool __(), все его экземпляры считаются истинными.
        """
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
