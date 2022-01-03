import re
import sys
'''
Скрипт индексирования текста. Пример функции setdefault
'''
WORD_RE = re.compile('\w+')

index = {}

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
#            occurrences = index.get(word, [])   # Получить список вхождений слова word или [], если не найден
#            occurrences.append(location)        # Добавить новое вхождение в  occurrences (случившееся)
#            index[word] = occurrences           # Поместить модифицированный список occurrences в словарь
            index.setdefault(word, []).append(location)

# d.setdefault(k, [default]) Если k принадлежит d, вернуть d[k], иначе положить d[k] = default и вернуть его значение

for word in sorted(index, key=str.upper):
    print(word, index[word])
