import random


class BingoCage:
    """
    Экземпляр этого класса строится из любого иттерируемого объекта и
    хранит внутри себя список элементов в случайном порядке. При вызове
    экземпляра из списка удаляется один элемент.
    """

    def __init__(self, items=None):
        """
        Метод __init__ принимает произвольный иттерируемый объект;
        Создание локальной копии предотвращает изменение списка, переданного
        в качестве аргумента.
        """
        self._items = list(items)
        random.shuffle(self._items)  # Метод shuffle гарантированно работает, т.к. self._items объект тип list.

    def pick(self):
        """
        Основной метод.
        """
        try:
            return self._items.pop()
        except IndexError:
            # Возбудить исключение со специальным сообщением, если список self._items пустой.
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        """
        Позволяет писать просто bingo() вместо bingo.pick()
        :return:
        """
        return self.pick()
