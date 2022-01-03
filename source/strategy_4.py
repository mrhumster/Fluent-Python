from source.strategy_3 import fidelity_promo, bulk_item_promo, large_order_promo
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
# promos - список стратегий реализованный в виде функций


def best_promo(order):
    """
    :param order: список покупок
    :return: максимально возможную скидку из params
    """
    return max(promo(order) for promo in promos)
