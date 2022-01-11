import abc


class Tombola(abc.ABC):
    """
    Что бы определить ABC, создаем подкласс `abc.ABC`

    doctest показывает не возможность создания экземпляра
    подкласса `Tombola` не реализующего абстрактные методы.

    >>> class Fake(Tombola):
    ...     def pick(self):
    ...         return 13
    ...
    >>> Fake
    <class '__main__.Fake'>
    >>> f = Fake()
    Traceback (most recent call last):
    ...
        f = Fake()
    TypeError: Can't instantiate abstract class Fake with abstract methods load, pick
    """
    @abc.abstractmethod
    def load(self, iterable):
        """
        Абстрактный метод помечен декоратором @abc.abstractmethod
        и зачастую содержит в теле только строку документации.

        :param iterable: добавляемый элемент в коллекцию.
        :return:
        """

    @abc.abstractmethod
    def pick(self):
        """
        Строка документации сообщает программисту, реализующему
        метод, что в случае отсутствия элементов, необходим
        возбудить `LookupError`.

        :return: случайный элементы из коллекции.
        Этот метод должен возбуждать исключение
        `LookupError`, если контейнер пуст.
        """

    def loaded(self):
        """
        ABC может содержать конкретные методы.

        :return: `True` если хотя бы 1 элемент, иначе `False`.
        """
        return bool(self.inspect())     # Конкретные методы ABC,
        # должны зависеть только от открытого интерфейса данного.

    def inspect(self):
        """
        :return: отсортированный кортеж, содержащий находящиеся
        в контейнере элементы
        """
        items = []
        while True:
            """
            Мы не знаем, как в конкретных подклассах будут храниться
            элементы, но можем построить `inspect` опустошив объект
            `Tombola` с помощью последовательного обращения методом 
            `.pick()`... 
            """
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        """
        ...а затем, с помощью `.load(...)` вернуть все элементы 
        обратно. 
        """
        return tuple(sorted(items))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
