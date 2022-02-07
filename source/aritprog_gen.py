def aritprog_gen(begin, step, end=None):
    """
    Реализация арифметической прогрессии
    с использованием генераторной функции.
    :param begin: начальное значение.
    :param step: шаг прогрессии.
    :param end: конечное значение
    (не обязательный аргумент)

    > Тест на проверку класса возвращаемеого значения
    >>> from fractions import Fraction
    >>> b = aritprog_gen(0, Fraction(1, 3), 1)
    >>> list(b)
    [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
    >>> from decimal import Decimal
    >>> c = aritprog_gen(0, Decimal('.01'), .03)
    >>> list(c)
    [Decimal('0'), Decimal('0.01'), Decimal('0.02')]
    """
    result = type(begin+step)(begin)
    # Возвращает значение того же класса,
    # что и начальное begin
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index
