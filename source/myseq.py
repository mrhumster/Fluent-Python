class MySeq:
    def __getitem__(self, item):
        """
        :param item: - индекс в последовательности.
        :return: в данном случае __getitem__ просто
        возвращает то, что ему передали.

        >>> s = MySeq()
        >>> s[1] # Один индекс, ничего нового.
        1
        >>> s[1:4] # Нотация 1:4 преобразуется в:
        slice(1, 4, None)
        >>> s[1:4:2] # slice(1, 4, 2) означает: начать с 1, закончить на 4, шаг 2.
        slice(1, 4, 2)
        >>> s[1:4:2, 9] # Сюрприз: при наличии запятых внутри [] метод __getitem__ принимает кортеж.
        (slice(1, 4, 2), 9)
        >>> s[1:4:2, 7:9] # Этот кортеж даже может содержать несколько объектов среза.
        (slice(1, 4, 2), slice(7, 9, None))
        """
        return item


if __name__ == '__main__':
    import doctest
    doctest.testmod()