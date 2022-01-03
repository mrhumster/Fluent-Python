#!./venv/Scripts/python.exe
# -*- coding: utf-8 -*-
"""
Паттерн ДЕКОРАТОР динамически наделяет объект новыми возможностями
и является гибкой альтернативой субклассирования в области расширения
функциональности.

Если нужен непараметризованный декоратор функции или метода, то просто
пишем фукнцию-декоратор, которая создает и возвращает обёртку.
Пример: @float_args_and_return

Если нужен параметризованный декоратор, то пишем фабрику декораторов,
которая создает декоратор.
Пример: @statically_typed(str, str, return_type=str)

"""
import functools


def float_args_and_return(func):
    """
    Аттрибут __name__ возвращенной декорированной функции содержит строку
    "wrapper", а не имя исходной функции. Что бы исправить в стандартной
    библиотеке python существует декорато @functools.wraps, который можно
    использовать для декорирования функции обертки. Он гарантирует, что
    аттрибут __name__ и __doc__ обертки содержат те же значения, что и
    аттрибуты исходной функции
    :param func: Декорируемая функция.
    :return: Декорированная функция.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = [float(arg) for arg in args]
        return float(func(*args, **kwargs))
    return wrapper


@float_args_and_return
def mean(first, second, *rest):
    """
    Декорировання функция mean() может приниать два и более
    аргумента любого типа, который преобразуется в float:
    mean(5, "6.4", "7"), не будь декоратора это обращеиние
    привело бы к исключению TypeError
    """
    numbers = (first + second) + rest
    return sum(numbers) / len(numbers)


def statically_typed(*types, return_type=None):
    """
    Фабрики декораторов создаются по единому образцу. Сначала мы создаем
    функцию-декоратор, а внутри неё функцию обертку, которая либо модифицируется,
    или подменяется. А функция-декорато возвращает обёртку. И наконец,
    фабрика декораторов возвращает сам декоратор.
    :param types: параметры с которыми должен быть создан декоратор
    :param return_type:
    :return: декоратор функции с требуемыми аргументами
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > len(types):
                raise ValueError("too many arguments")
            elif len(args) < len(types):
                raise ValueError("too few arguments")
            for i, (arg, type_) in enumerate(zip(args, types)):
                if not isinstance(arg, type_):
                    raise ValueError(f"argument {i} must be of type {type_.__name__}")
            result = func(*args, **kwargs)
            if return_type is not None and not isinstance(result, return_type):
                raise ValueError(f"return value must be of type {return_type.__name__}")
            return result
        return wrapper
    return decorator


@statically_typed(str, str, return_type=str)
def make_tagged(text, tag):
    return f'<{tag}>{text}</{tag}>'


@statically_typed(str, int, str)
def repeat(what, count, separator):
    return ((what + separator) * count)[:-len(separator)]
