import keyword

from explore0 import FrozenJSON


class FrozenJSON1(FrozenJSON):

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value
