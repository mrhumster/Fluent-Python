from random import randrange
from tombola import Tombola


@Tombola.register           # Виртуальная регистрация как подкласс Tombola
class TomboList(list):
    """
    Пример реализации виртуального подкласса.
    Важно для корректности реализовать все методы из ABC.

    >>> from tombola import Tombola
    >>> t = TomboList(range(100))
    >>> isinstance(t, Tombola)
    True

    """
    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend          # Хитрое выражение >;)

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
