def quantity(storage_name):
    """
    :param storage_name: определяет, где хранятся
    данные свойства; в случае свойства weight данные
    будут храниться в атрибуте с именем 'weight'.

    :return: Конструируем и возвращаем объект свойства.
    """
    def qty_getter(instance):
        """
        Называть первым аргумент метода qty_getter
        именем self было бы не совсем правильно,
        т.к. это не тело класса;

        :param instance: ссылается на экземпляр
        LineItem, в котором будет храниться объект.

        :return: метод ссылается на storage_name,
        поэтому будет сохранён в замыкании этой функции;
        значение берётся непосредственно из instance.__dict__,
        чтобы обойти свойство и избежать бесконечной рекурсии.
        """
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    """
    Используем фабрику для определения первого
    свойства, weight, в виде атрибута класса.
    """
    weight = quantity('weight')
    # Здесь создаётся второе свойство, price.
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        """
        Здесь свойство уже работает, и поэтому 
        попытка присвоить weight нулевое или 
        отрицательное значение отвергается.
        """
        self.weight = weight
        self.price = price

    def subtotal(self):
        """
        Здесь свойства также работают: с их
        помощью производится доступ к значениям,
        хранящимся в экземпляре.
        """
        return self.weight * self.price

