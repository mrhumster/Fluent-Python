import abc


class AutoStorage:
    """
    Класс AutoStorage предоставляет большую часть
    функциональности бывшего дескриптора Quantity
    за исключением проверки.
    """
    __counter = 0

    def __int__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'_{prefix}#{index}'
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    """
    Класс абстрактный и наследует AutoStorage
    """
    def __set__(self, instance, value):
        """
        Делегирует проверку методу validate, а затем передаёт
        значение value методу __set__ суперкласса, который и
        производит сохранение.
        :param instance:
        :param value:
        :return:
        """
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """Возвращает проверенное значение или возбуждает ValueError"""


class Quantity(Validated):
    """Число больше нуля"""
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """Строка содержит хотя бы один не пробельный символ"""
    def validate(self, instance, value):
        """
        Требуя, чтобы конкретные методы validate возвращали
        проверенное значение, мы оставляем им возможность
        очистить, преобразовать или нормализовать полученные
        данные. В данном случае значение value перед возвратом
        очищается от начальных и конечных пробелов.
        :param instance:
        :param value:
        :return:
        """
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value
