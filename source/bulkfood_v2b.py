class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.wight = weight
        self.price = price

    def subtotal(self):
        return self.wight * self.price

    def get_weight(self):
        # Простой метод чтения
        return self.__weight

    def set_weight(self, value):
        # Простой метод установки
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    # Строим свойство и присваиваем его открытому атрибуту класса.
    weight = property(get_weight, set_weight)
