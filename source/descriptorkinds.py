# Вспомогательные функции для отображения
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__[{pseudo_args}]')


# Существенные для этого примера классы
class Overriding:
    """
    Типичный переопределяющий дескрипторный класс с методами __get__ и __set__.
    Он же дескриптор данных или принудительный дескриптор

    *** Тестирование переопределяющего дескриптора ***

    >>> obj = Managed()     # Cоздаём объект Managed для тестирования
    >>> obj.over            # obj.over активирует метод дескриптора __get__, передавая ему управляемый экземпляр obj во втором аргументе.
    -> Overriding.__get__[<Overriding object>, <Managed object>, <class Managed>]
    >>> Managed.over        # Managed.over активирует метод дескриптора __get__, передавая ему None во втором аргументе (instance).
    -> Overriding.__get__[<Overriding object>, None, <class Managed>]
    >>> obj.over = 7        # Присваивание obj.over активирует метод дескриптора __set__, передавая ему значение 7 в последнем аргументе.
    -> Overriding.__set__[<Overriding object>, <Managed object>, 7]
    >>> obj.over            # Чтение obj.over по-прежнему активирует метод дескриптора __get__.
    -> Overriding.__get__[<Overriding object>, <Managed object>, <class Managed>]
    >>> obj.__dict__['over'] = 8    # Установка значения непосредственно в obj.__dict__ в обход дескриптора.
    >>> vars(obj)           # Проверяем, что значение попало в obj.__dict__ и ассоциировано с ключом over.
    {'over': 8}
    >>> obj.over            # *** Однако даже при наличии атрибута экземпляра с именем over дескриптор Managed.over всё равно переопределяет попытки читать obj.over.
    -> Overriding.__get__[<Overriding object>, <Managed object>, <class Managed>]

    """
    def __get__(self, instance, owner):
        """
        В этом примере функция print_args вызывается из каждого метода дескриптора.
        """
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """
    Переопределяющий дескриптор без __get__

    *** Тестирование переопределяющего дескриптора без  __get__ ***

    В этои переопределяющем дескрипторе нет метода __get__, поэтому чтение
    obj.over_no_get извлекает экземпляр дескрипторп из класса.

    >>> obj = Managed()
    >>> obj.over_no_get         #doctest: +ELLIPSIS
    <__main__.OverridingNoGet object at 0x...>
    >>> Managed.over_no_get     #doctest: +ELLIPSIS
    <__main__.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7     # Попытка присвоить значение атрибуту obj.over_no_get активирует метод дескриптора __set__.
    -> OverridingNoGet.__set__[<OverridingNoGet object>, <Managed object>, 7]
    >>> obj.over_no_get         # Поскольку наш метод __set__ не производит никаких изменений, повторное чтение obj.over_no_get извлекает всё тот же экземпляр дескриптора из управляемого класса. #doctest: +ELLIPSIS
    <__main__.OverridingNoGet object at 0x...>
    >>> obj.__dict__['over_no_get'] = 9     # Устанавливаем атрибут экземпляра с именем over_no_get через атрибут __dict__ экземпляра.
    >>> obj.over_no_get         # Теперь новый атрибут экземпляра over_no_get маскирует дескриптор, но только при чтении.
    9
    >>> obj.over_no_get = 7     # Попытка присвоить значение атрибуту obj.over_no_get по-прежнему проходит через метод __set__ дескрипторп.
    -> OverridingNoGet.__set__[<OverridingNoGet object>, <Managed object>, 7]
    >>> obj.over_no_get         # Но при чтении дескриптор замаскирован до тех пор, пока существует одноименный атрибут экземпляра.
    9
    """
    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    """
    Здесь нет метода __set__, т.е. этот дескриптор не переопределяющий.
    Он же дескриптор без данных или маскируемый дескриптор

    *** Тестирование не переопределяющего дескриптора ***

    >>> obj = Managed()
    >>> obj.non_over        # obj.non_over активирует метод дескриптора __get__, передавая ему obj во втором аргументе.
    -> NonOverriding.__get__[<NonOverriding object>, <Managed object>, <class Managed>]
    >>> obj.non_over = 7    # Managed.non_over -- не переопределяющий дескриптор, поэтому не существует метода __set__, который могбы вмешаться в эту операцию присваивания.
    >>> obj.non_over        # Теперь в obj есть атрибут экземпляра с именем non_over, который маскирует одноименный дескрипторный атрибут в классе Managed.
    7
    >>> Managed.non_over    # Дескрипторный Managed.non_over по-прежнему существует и перехватывает эту операцию доступа через класс.
    -> NonOverriding.__get__[<NonOverriding object>, None, <class Managed>]
    >>> del obj.non_over    # Если удалить атрибут экземпляра non_over то чтение obj.non_over активирует
    >>> obj.non_over        # метод __get__ дескриптора в классе, однако вторым аргументом будет управляемый экземпляр.
    -> NonOverriding.__get__[<NonOverriding object>, <Managed object>, <class Managed>]

    """
    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    """
    Управляющий класс, в котором используется по
    одному экземпляру каждого дескрипторного класса.
    """
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        """
        Метод spam включён для сравнения, потому
        что методы -- также дескрипторы.
        """
        print(f'-> Managed.spam({display(self)})')


if __name__ == '__main__':
    import doctest
    doctest.testmod()