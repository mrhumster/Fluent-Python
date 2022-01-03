promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']
"""
promos - перебираем все имена в словаре, 
возвращенном функцией global(), оставляем 
только те что с суффикосом _promo и не best_promo
"""


def best_promo(order):
    """
    :param order: список покупок
    :return: максимально возможную скидку из params
    """
    return max(promo(order) for promo in promos)
