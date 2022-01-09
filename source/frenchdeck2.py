from abc import ABC
from collections import abc, namedtuple

Card = namedtuple('Card', ['rank', 'suit'])
"""
Card -- мини-класс карты

namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
    Возвращает новый подкласс кортежа с именованными полями.
    
    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
"""


class FrenchDeck2(abc.MutableSequence, ABC):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamond clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]

    def __setitem__(self, key, value):
        """
        Данный метод, всё что нужно для поддержки
        тасования (random.shuffle)
        :param key: - позиция карты
        :param value: - карта
        >>> deck = FrenchDeck2()
        >>> from random import shuffle
        >>> shuffle(deck)
        """
        self._cards[key] = value

    def __delitem__(self, key):
        """
        Что бы создать подкласс abc.MutableSequence
        необходимо так же реализовать метод удаления
        карты из колоды.
        :param key: - позиция карты
        """
        del self._cards[key]

    def insert(self, index: int, value: Card) -> None:
        """
        Так же необходимо реализовать третий абстрактный
        метод abc.MutableSequence
        """
        self._cards.insert(index, value)
