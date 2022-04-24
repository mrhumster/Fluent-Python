class BlackKnight:

    def __init__(self):
        """
        >>> knight = BlackKnight()
        >>> knight.member
        следующий член:
        'рука'
        >>> del knight.member
        ЧЕРНЫЙ РЫЦАРЬ (утрачена рука)
        -- Это всего лишь царапина.
        >>> del knight.member
        ЧЕРНЫЙ РЫЦАРЬ (утрачена вторая рука)
        -- Это всего лишь поверхностная рана.
        >>> del knight.member
        ЧЕРНЫЙ РЫЦАРЬ (утрачена нога)
        -- Я неуязвим!
        >>> del knight.member
        ЧЕРНЫЙ РЫЦАРЬ (утрачена вторая нога)
        -- Ну ладно, пусть будет ничья.
        """
        self.members = [
            'рука', 'вторая рука',
            'нога', 'вторая нога'
        ]
        self.phrases = [
            'Это всего лишь царапина.',
            'Это всего лишь поверхностная рана.',
            'Я неуязвим!',
            'Ну ладно, пусть будет ничья.'
        ]

    @property
    def member(self):
        print('следующий член:')
        return self.members[0]

    @member.deleter
    def member(self):
        print(f'ЧЕРНЫЙ РЫЦАРЬ (утрачена {self.members.pop(0)})\n-- {self.phrases.pop(0)}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()