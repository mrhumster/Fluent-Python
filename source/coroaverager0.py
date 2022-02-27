def averager():
    """
    >>> coro_avg = averager()
    >>> next(coro_avg)          # Init generator
    >>> coro_avg.send(10)
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0
    :return:
    """

    total = .0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
