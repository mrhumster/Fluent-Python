def http_error(status):
    """
    Switch Case is Here!

    https://www.python.org/dev/peps/pep-0636/

    >>> http_error(500)
    "Something's wrong with the Internet"
    >>> http_error(400)
    'Bad request'
    """
    match status:
        case 400:
            return "Bad request"
        case 401 | 403:
            return "Not allowed"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the Internet"


def zip_length_check():
    """
    strict - проверка на длину последовательностей

    https://www.python.org/dev/peps/pep-0618/

    >>> x = [1, 2, 3, 4]
    >>> y = [5, 7, 8]
    >>> list(zip(x, y))
    [(1, 5), (2, 7), (3, 8)]
    >>> list(zip(x, y, strict=True))
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    ValueError: zip() argument 2 is shorter than argument 1
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()