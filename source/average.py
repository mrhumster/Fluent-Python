def make_averager():
    """
    При обращении к make_averager возвращается объект-функция averager.
    При каждом вызове averager добавляет переданный аргумент в конец
    списка series и вычисляет текущее среднее.
    :return:
    """
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager
