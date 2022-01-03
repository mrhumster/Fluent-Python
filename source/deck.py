import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])
"""
collections.namedtuple - используется для коструирования простого класса, представляющего одну карту.
Можно использовать для построения классов, содержащий только аттрибуты и никаких методов. прим.: запись БД.
"""


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'черви буби крести пики'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]
