class Quantity:
    """
    Дескриптор основан на протоколе,
    для его реализации не требуется
    наследование.
    """
    def __init__(self, storage_name):
        """
        :param storage_name: имя атрибута, в котором
        хранится значение управляемого экземпляра.
        """
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """
        Вызывается при любой попытке присвоить значение управляемому атрибуту.
        :param instance: управляемый экземпляр.
        :param value: присваиваемое значение.
        :return:
        """
        if value > 0:
            """
            Здесь мы должны работать с атрибутом __dict__ управляемого экземпляра напрямую;
            попытка воспользоваться встроенной функцией setattr привела бы к повторному 
            вызову метода __set__ и, стало быть, к бесконечной рекурсии.
            """
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
