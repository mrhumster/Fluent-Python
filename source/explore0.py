from collections import abc


class FrozenJSON:
    """
    Допускающий только чтение фасад для навигации по
    JSON-подобному объекту с применением нотации атрибутов
    """

    def __init__(self, mapping):
        """
        Строим объект dict по аргументу mapping. Тем самым
        мы решаем 2 задачи: проверяем, что получили словарь
        и для безопасности делаем его копию.
        """
        self.__data = dict(mapping)

    def __getattr__(self, item):
        """
        Метод вызывается только когда не существует атрибута
        с таким именем.
        """
        if hasattr(self.__data, item):
            return getattr(self.__data, item)
        else:
            return FrozenJSON.build(self.__data[item])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
