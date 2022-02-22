import contextlib


@contextlib.contextmanager
def looking_glass():

    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        """
        >>> from mirror_gen import looking_glass
        >>> with looking_glass() as what:
        ...     print('шалаш')
        ...     print(what)
        шалаш
        РАКОМ ДЕД ЕБЕТ КОБЫЛУ
        >>> what
        'УЛЫБОК ТЕБЕ ДЕД МОКАР'
        >>> print('Back to normal')
        Back to normal
        """
        original_write(text[::-1])
        sys.stdout.write = reverse_write
        yield 'УЛЫБОК ТЕБЕ ДЕД МОКАР'   # Отдаем значение, которое
        # будет связано с переменной в части as предложения with.
        # В этой точке функция приостанавливается на время
        # выполнения блока with.
        sys.stdout.write = original_write   # Всё что идет после
        # yield выполняется после блока with


if __name__ == '__main__':
    import doctest
    doctest.testmod()

