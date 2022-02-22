class LookingGlass:
    """
    >>> from mirror import LookingGlass
    >>> with LookingGlass() as what:
    ...     print('шалаш')
    ...     print(what)
    шалаш
    РАКОМ ДЕД ЕБЕТ КОБЫЛУ
    >>> what
    'УЛЫБОК ТЕБЕ ДЕД МОКАР'
    >>> print('Back to normal')
    Back to normal
    """

    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'УЛЫБОК ТЕБЕ ДЕД МОКАР'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):  # Python вызывает метод __exit__
        # с аргументами None, None, None, если не было ошибок; если было исключение,
        # то в аргументах передаются данные об исключении
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Division by zero')
            return True     # Посылаем True, что бы интерпретатор знал об обработке
            # исключения. Если метод __exit__ возвращает None или вообще что-нибудь,
            # кроме True, то исключение возникшее внутри блока with, распространяется дальше.


if __name__ == '__main__':
    import doctest
    doctest.testmod()
