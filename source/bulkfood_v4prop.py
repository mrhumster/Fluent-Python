def quantity():                 # Аргумента storage_name нет
    try:                        # Мы не можем полагаться на атрибут
        quantity.counter += 1   # класса для сохранения счётчика между
    except AttributeError:      # вызовами, поэтому определим эту переменную
        quantity.counter = 0    # как атрибут самой функции quantity. Если счетчик
                                # не определён, присваиваем переменной значение 0.
    """
    Атрибутов экземпляра у нас тоже нт, поэтому создаём 
    storage_name, как локальную переменную, а в qty_getter 
    и qty_setter её значение будет доступно благодаря замыканию.
    """
    storage_name = f'_quantity:{quantity.counter}'
    """
    Остальной код отличается от предыдущей реализации, только тем, 
    что мы можем использовать встроенные функции getattr и  setattr, 
    а не манипулировать напрямую атрибутом instance.__dict___.
    """
    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)