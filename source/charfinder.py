#!/usr/bin/env python3

"""
Unicode character finder utility:
find characters based on words in their official names.

This can be used from the command line, just past words as arguments.

Here is the ``main`` function which makes it happen::

>>> main('rook') # doctest: +NORMALIZE_WHITESPACE
U+2656      ♖       WHITE CHESS ROOK
(1 match for rook)
U+265C      ♜       BLACK CHESS ROOK
(2 matches for rook)
U+1FA02     🨂       NEUTRAL CHESS ROOK
(3 matches for rook)
U+1FA0B     🨋       WHITE CHESS ROOK ROTATED NINETY DEGREES
(4 matches for rook)
U+1FA11     🨑       BLACK CHESS ROOK ROTATED NINETY DEGREES
(5 matches for rook)
U+1FA17     🨗       NEUTRAL CHESS ROOK ROTATED NINETY DEGREES
(6 matches for rook)
U+1FA20     🨠       WHITE CHESS TURNED ROOK
(7 matches for rook)
U+1FA26     🨦       BLACK CHESS TURNED ROOK
(8 matches for rook)
U+1FA2C     🨬       NEUTRAL CHESS TURNED ROOK
(9 matches for rook)
U+1FA35     🨵       WHITE CHESS ROOK ROTATED TWO HUNDRED SEVENTY DEGREES
(10 matches for rook)
U+1FA3B     🨻       BLACK CHESS ROOK ROTATED TWO HUNDRED SEVENTY DEGREES
(11 matches for rook)
U+1FA41     🩁       NEUTRAL CHESS ROOK ROTATED TWO HUNDRED SEVENTY DEGREES
(12 matches for rook)
U+1FA4F     🩏       WHITE CHESS KNIGHT-ROOK
(13 matches for rook)
U+1FA52     🩒       BLACK CHESS KNIGHT-ROOK
(14 matches for rook)
>>> main('rook', 'black') # doctest: +NORMALIZE_WHITESPACE
U+265C      ♜       BLACK CHESS ROOK
(1 match for rook black)
U+1FA11     🨑       BLACK CHESS ROOK ROTATED NINETY DEGREES
(2 matches for rook black)
U+1FA26     🨦       BLACK CHESS TURNED ROOK
(3 matches for rook black)
U+1FA3B     🨻       BLACK CHESS ROOK ROTATED TWO HUNDRED SEVENTY DEGREES
(4 matches for rook black)
U+1FA52     🩒       BLACK CHESS KNIGHT-ROOK
(5 matches for rook black)
>>> main('white bishop') # doctest: +NORMALIZE_WHITESPACE
U+2657      ♗       WHITE CHESS BISHOP
(1 match for white bishop)
U+1FA0C     🨌       WHITE CHESS BISHOP ROTATED NINETY DEGREES
(2 matches for white bishop)
U+1FA21     🨡       WHITE CHESS TURNED BISHOP
(3 matches for white bishop)
U+1FA36     🨶       WHITE CHESS BISHOP ROTATED TWO HUNDRED SEVENTY DEGREES
(4 matches for white bishop)
U+1FA50     🩐       WHITE CHESS KNIGHT-BISHOP
(5 matches for white bishop)



For exploring words that occur in the character names, there is the
``word_report`` function::

>>> index = UnicodeNameIndex(sample_chars)
>>> index.word_report()
    3 SIGN
    2 A
    2 EURO
    2 LATIN
    2 LETTER
    1 CAPITAL
    1 CURRENCY
    1 DOLLAR
    1 SMALL
>>> index = UnicodeNameIndex()
>>> index.word_report(10)
94061 CJK
94001 IDEOGRAPH
92896 UNIFIED
13394 SYLLABLE
11735 HANGUL
10350 LETTER
 3245 SIGN
 3090 SMALL
 2524 WITH
 1977 CAPITAL

Note: characters with names starting with 'CJK UNIFIED IDEOGRAPH'
are indexed with those three words only, excluding the hexadecimal
codepoint at the end of the name.

"""

import sys
import re
import unicodedata
import pickle
import warnings
import itertools
import functools
from collections import namedtuple

RE_WORD = re.compile('\w+')
RE_UNICODE_NAME = re.compile('^[A-Z0-9 -]+$')
RE_CODEPOINT = re.compile('U\+([0-9A-F]{4,6})')

INDEX_NAME = 'charfinder_index.pickle'
MINIMUM_SAVE_LEN = 10000
CJK_UNI_PREFIX = 'CJK UNIFIED IDEOGRAPH'
CJK_CMP_PREFIX = 'CJK COMPATIBILITY IDEOGRAPH'

sample_chars = [
    '$',        # DOLLAR SIGN
    'A',        # LATIN CAPITAL LETTER A
    'a',        # LATIN SMALL LETTER A
    '\u20a0',   # EURO-CURRENCY SIGN
    '\u20ac',   # EURO SIGN
]

CharDescription = namedtuple('CharDescription', 'code_str char name')

QueryResult = namedtuple('QueryResult', 'count items')


def tokenize(text):
    """return iterable of uppercased words"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()


def query_type(text):
    text_upper = text.upper()
    if 'U+' in text_upper:
        return 'CODEPOINT'
    elif RE_UNICODE_NAME.match(text_upper):
        return 'NAME'
    else:
        return 'CHARACTERS'


class UnicodeNameIndex:

    def __init__(self, chars=None):
        self.load(chars)

    def load(self, chars=None):
        self.index = None
        if chars is None:
            try:
                with open(INDEX_NAME, 'rb') as fp:
                    self.index = pickle.load(fp)
            except OSError:
                pass

        if self.index is None:
            self.build_index(chars)

        if len(self.index) > MINIMUM_SAVE_LEN:
            try:
                self.save()
            except OSError as exc:
                warnings.warn(f'Could not save {INDEX_NAME}: {exc}')

    def save(self):
        with open(INDEX_NAME, 'wb') as fp:
            pickle.dump(self.index, fp)

    def build_index(self, chars=None):
        if chars is None:
            chars = (chr(i) for i in range(32, sys.maxunicode))
        index = {}
        for char in chars:
            try:
                name = unicodedata.name(char)
            except ValueError:
                continue
            if name.startswith(CJK_UNI_PREFIX):
                name = CJK_UNI_PREFIX
            elif name.startswith(CJK_CMP_PREFIX):
                name = CJK_CMP_PREFIX

            for word in tokenize(name):
                index.setdefault(word, set()).add(char)

        self.index = index

    def word_rank(self, top=None):
        res = [(len(self.index[key]), key) for key in self.index]
        res.sort(key=lambda item: (-item[0], item[1]))
        if top is not None:
            res = res[:top]
        return res

    def word_report(self, top=None):
        for postings, key in self.word_rank(top):
            print(f'{postings:5} {key}')

    def find_chars(self, query, start=0, stop=None):
        stop = sys.maxsize if stop is None else stop
        result_sets = []
        for word in tokenize(query):
            chars = self.index.get(word)
            if chars is None:       # shortcut: no such word
                result_sets = []
                break
            result_sets.append(chars)

        if not result_sets:
            return QueryResult(0, ())

        result = functools.reduce(set.intersection, result_sets)
        result = sorted(result)     # must sort to support start, stop
        result_iter = itertools.islice(result, start, stop)
        return QueryResult(len(result), (char for char in result_iter))

    def describe(self, char):
        code_str = 'U+{:04X}'.format(ord(char))
        name = unicodedata.name(char)
        return CharDescription(code_str, char, name)

    def find_descriptions(self, query, start=0, stop=None):
        for char in self.find_chars(query, start, stop).items:
            yield self.describe(char)

    def get_descriptions(self, chars):
        for char in chars:
            yield self.describe(char)

    def describe_str(self, char):
        return '{:7}\t{}\t{}'.format(*self.describe(char))

    def find_description_strs(self, query, start=0, stop=None):
        for char in self.find_chars(query, start, stop).items:
            yield self.describe_str(char)

    @staticmethod       # not an instance method due to concurrency
    def status(query, counter):
        if counter == 0:
            msg = 'No match'
        elif counter == 1:
            msg = '1 match'
        else:
            msg = f'{counter} matches'
        return f'{msg} for {query}'


def main(*args):
    index = UnicodeNameIndex()
    query = ' '.join(args)
    n = 0
    for n, line in enumerate(index.find_description_strs(query), 1):
        print(line)
        print('({})'.format(index.status(query, n)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        print(f'Usage: {sys.argv[0]} word1 [word2]...')
