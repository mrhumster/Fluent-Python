import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
        # Возвращает список всех не пересекающихся
        # подстрок, соответствующих регулярному выражению RE_WORD.

    def __getitem__(self, item):
        """
        self.words содержит результат .fandall, поэтому мы просто
        возвращаем слово с заданным индексом
        """
        return self.words[item]

    def __len__(self):
        """
        Что бы выполнить требования протокола последовательности,
        реализуем данный метод,- но для получения итерируемого
        объекта он не нужен.
        """
        return len(self.words)

    def __repr__(self):
        """
        По умолчанию reprlib.repr ограничивает сгенерированную
        строку 30 символами.
        >>> s = Sentence('Время жизни на репит, просто что бы закрепить.')
        >>> s
        Sentence('Время жизни ...бы закрепить.')
        >>> for word in s:
        ...     print(word)
        ...
        Время
        жизни
        на
        репит
        просто
        что
        бы
        закрепить
        >>> list(s)
        ['Время', 'жизни', 'на', 'репит', 'просто', 'что', 'бы', 'закрепить']
        """
        return 'Sentence(%s)' % reprlib.repr(self.text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
