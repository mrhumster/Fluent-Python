class LineItem:

    def __init__(self, description, weight, price):
        """
        Здесь уже используется метод установки свойства,
        который гарантирует, что не будет создан экземпляр
        с отрицательным значением weight
        """
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.price * self.weight

    @property   # Декоратор @property обозначает метод чтения свойства.
    def weight(self):
        """
        Имена всех методов, реализующих свойство, совпадают с именем
        открытого атрибута: weight
        Фактическое значение хранится в закрытом атрибуте self.__weight
        """
        return self.__weight

    @weight.setter
    def weight(self, value):
        """
        У декорированного метода чтения свойства имеется атрибут
        .setter, который является также и декоратором; тем самым
        методы чтения и установки связываются между собой.
        """
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
