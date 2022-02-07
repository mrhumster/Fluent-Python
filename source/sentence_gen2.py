import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        """
        Ленивая реализация класса Sentence.
        Хранить список слов не нужно.
        """
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        """
        finditer строит итератор, который обходит все
        соответствия текста self.text регулярному выражению
        RE_WORD, порождая объекты MatchObject.

        match.group() извлекает сопоставленный текст из
        объекта MatchObject
        """
        for match in RE_WORD.finditer(self.text):
            yield match.group()
