from collections import abc
from keyword import iskeyword


class FrozenJSON:
    """
    Допускающий только чтение фасад для навигации по
    JSON-подобному объекту с применением нотации атрибутов.
    """

    def __new__(cls, arg):
        """
        Будучи методом класса, __new__ получает в качестве
        первого аргумента сам класс, а остальные аргументы
        - те же, что получает __init__, за исключением self.
        """
        if isinstance(arg, abc.Mapping):
            """
            По умолчанию работа делегируется методу __new__
            суперкласса. В данном случае мы вызываем метод
            __new__ из базового класса object, передавая
            ему FrozenJSON в качестве единственного аргумента.
            """
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableMapping):
            """
            Оставшаяся часть __new__ ничем не отличается от
            прежнего метода build.
            """
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, item):
        if hasattr(self.__data, item):
            return getattr(self.__data, item)
        else:
            """
            Здесь раньше вызывался метод FrozenJSON.build,
            а теперь мы просто вызываем конструктор FrozenJSON.
            """
            return FrozenJSON(self.__data[item])
