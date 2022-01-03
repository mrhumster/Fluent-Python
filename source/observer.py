#!./venv/Scripts/python.exe
# -*- coding: utf-8 -*-
"""
Паттерн НАБЛЮДАТЕЛЬ определяет отношение "один-ко-многим" между
объектами, таким  образом,  что  при изменении состояния одного
объекта происходит  автоматическое оповещение и обновление всех
зависимых объектов.
"""
import datetime
import itertools
import sys
import time


class Observed:
    """
    Этот класс предназначен на роль базового для моделей и любых
    других классов, которые хотят поддержать наблюдение.
    """
    def __init__(self):
        self.__observers = set()    # Пустое множество

    def observers_add(self, observer, *observers):
        """
        Мы хотим иметь возможность добавлять одного или более наблюдателей.
        Но если бы написали просто *observers,то можно было бы добавить 0
        или более наблюдателей.

        :param observer: Хотя бы один наблюдатель был.
        :param observers: А сверх него готовы принять 0 или более

        itertools.chain() принимает произвольное колличество итеррируемых
        объектов и возврящает единственный иттерируемы объект, который ведет
        себя как их конкатенация.
        """
        for observer in itertools.chain((observer,), observers):
            self.__observers.add(observer)
            observer.update(self)

    def observer_discard(self, observer):
        # Удаление элемента из множества, если таковое присутсвует
        self.__observers.discard(observer)

    def observers_notify(self):
        for observer in self.__observers:
            observer.update(self)


class SliderModel(Observed):

    def __init__(self, minimum, value, maximum):
        super().__init__()
        self.__minimum = self.__value = self.__maximum = None
        self.minimum = minimum
        self.value = value
        self.maximum = maximum

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.__value != value:
            self.__value = value
            self.observers_notify()

    @property
    def minimum(self):
        return self.__minimum

    @minimum.setter
    def minimum(self, minimum):
        if self.__minimum != minimum:
            self.__minimum = minimum
            self.observers_notify()

    @property
    def maximum(self):
        return self.__maximum

    @maximum.setter
    def maximum(self, maximum):
        if self.__maximum != maximum:
            self.__maximum = maximum
            self.observers_notify()


class HistoryView:
    """
    Это представление является наблюдателем модели, потому что представлен
    метод update(), который принимает наблюдаемую модель в качестве единственного
    аргумента, помимо self
    """
    def __init__(self):
        self.data = []

    def update(self, model):
        self.data.append((model.value, time.time()))


class LiveView:
    """
    Это еще одно представление, наблюдающее за моделью. Параметр length - это
    количество ячеек для представления значения модели в HTML-таблице с одной строкой.
    """
    def __init__(self, length=40):
        self.length = length

    def update(self, model):
        tippingPoint = round(model.value * self.length / (model.maximum - model.minimum))
        td = '<td style="background-color: {}">&nbsp;</td>'
        html = ['<table style="font-family: monospace" border="0"><tr>']
        html.extend(td.format("darkblue") * tippingPoint)
        html.extend(td.format("cyan") * (self.length - tippingPoint))
        html.append(f"<td>{model.value}</td></tr></table>")
        print("".join(html))


def main():
    historyView = HistoryView()
    liveView = LiveView()
    model = SliderModel(0, 0, 40)   # min, значение, max
    model.observers_add(historyView, liveView) # liveView
    for value in (7, 23, 37):                  # пораждает вывод
        model.value = value
    for value, timestamp in historyView.data:
        print(f'{value:3} {datetime.datetime.fromtimestamp(timestamp)}', file=sys.stderr)


if __name__ == '__main__':
    main()
