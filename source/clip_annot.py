def clip(text: str, max_len: 'int > 0' = 80) -> str:  # Аннотированное объявление функции
    """
    Return text clipped at the last space before or after max_len

    :param text:
        Переменная с текстом
    :param max_len:
        Максимальная длина возвращаемой строки
    :return:
        Возращает строку обрезаную до последнего пробела или до максимальной длины.
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # No spaces were found
        end = len(text)
    return text[:end].rstrip()
