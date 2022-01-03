#!./venv/Scripts/python.exe
# -*- coding: utf-8 -*-
"""
Паттерн СТРАТЕГИЯ определяет семейство алгоритмов, инкапсулирует
каждый из них и обеспечивает их взаимозаменяемость. Он позволяет
модифицировать алгоритмы независимо от их использования на стороне клиента.
"""
COLLEAGUES = ('Павел Клименко', 'Павел Румянцев', 'Николай Ластовский',
              'Кирилл Кулешов', 'Сергей Мирук', 'Алёна Ларина')


class Layout:
    """
    Этот класс поддерживает только один алгоритм: табуляция. Функция,
    реализующая этот алгоритм, ожидает получить счетчик строк и после-
    довательность элементов, а возвращает результат в виде таблицы.
    """
    def __init__(self, tabulator):
        self.tabulate = tabulator

    def tabulate(self, rows, items):
        return self.tabulator(rows, items)


def main():
    """
    В этой функции создаются 2 объекта Layout, параметризованные
    различными функциями-табуляторами. Для каждого формата печатается
    таблица с 2,3,4,5 строками
    :return:
    """
    htmlLayout = Layout(html_tabulator)
    for rows in range(2, 6):
        print(htmlLayout.tabulate(rows, COLLEAGUES))
    textLayout = Layout(text_tabulator)
    for rows in range(2, 6):
        print(textLayout.tabulate(rows, COLLEAGUES))
