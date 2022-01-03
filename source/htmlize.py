from collections import abc
import html
import numbers
from functools import singledispatch


@singledispatch             # Помечает базовую функцию, которая обрабатывает obj
def htmlize(obj):
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'


@htmlize.register(str)      # Каждая специальная функция снабжается декоратором
def _(text):                # Имена функций не существенны
    content = html.escape(text).replace('\n', '<br>\n')
    return f'<pre>{content}</pre>'


@htmlize.regiter(numbers.Integral)
def _(n):
    return f'<pre>{n} (0x{0:x})</pre>'


@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return f'<ul>\n<li>{inner}</li>\n<li>'
