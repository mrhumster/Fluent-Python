from functools import wraps


def coroutine(func):
    """Decorator: primes `func` by advancing to first `yield`"""
    @wraps(func)
    # Декорированная функция подменяется этой функцией primer
    def primer(*args, **kwargs):
        # Вызываем декорируемую функцию, что бы получить инициализированный генератор
        gen = func(*args, **kwargs)
        # Инициализируем генератор
        next(gen)
        # Возвращаем его
        return gen
    return primer
