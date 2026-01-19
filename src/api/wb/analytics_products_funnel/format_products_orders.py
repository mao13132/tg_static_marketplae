# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Преобразует ответ products (sales-funnel/products) к формату:
#   [{'nmID': <int>, 'history': [{'ordersCount': <int>, 'ordersSumRub': <float> }]}]
# - Берём агрегированные значения из блока statistic.selected.
# ---------------------------------------------
from collections import defaultdict


def _extract_nmid(product):
    # Пробуем достать артикул (nmID) из блока "product"
    for key in ('nmID', 'nmId', 'id', 'nmid'):
        try:
            val = product.get(key)
        except Exception:
            val = None
        if val is not None:
            try:
                return int(val)
            except Exception:
                pass
    return None


def format_products_orders_to_history(all_chunks_response, requested_nmids):
    # all_chunks_response: список ответов (каждый ответ — dict с ключом data.products)
    # requested_nmids: исходный список артикулов для фильтрации
    #
    # Возвращает список словарей:
    # - nmID
    # - history: [{ ordersCount, ordersSumRub }]

    requested = set(requested_nmids or [])

    agg = defaultdict(lambda: {'ordersCount': 0, 'ordersSumRub': 0.0})

    for resp in all_chunks_response or []:
        if not resp:
            continue

        try:
            products = (resp.get('data') or {}).get('products') or []
        except Exception:
            products = []

        for item in products:
            try:
                product = item.get('product') or {}
                statistic = item.get('statistic') or {}
                selected = statistic.get('selected') or {}
            except Exception:
                continue

            nmid = _extract_nmid(product)
            if nmid is None:
                continue

            if requested and nmid not in requested:
                continue

            try:
                orders = int(selected.get('orderCount') or 0)
            except Exception:
                orders = 0
            try:
                money = float(selected.get('orderSum') or 0)
            except Exception:
                money = 0.0

            agg[nmid]['ordersCount'] += orders
            agg[nmid]['ordersSumRub'] += money

    result = []
    for nmid, metrics in agg.items():
        result.append({
            'nmID': nmid,
            'history': [
                {
                    'ordersCount': int(metrics['ordersCount']),
                    'ordersSumRub': round(float(metrics['ordersSumRub']), 2),
                }
            ]
        })

    return result

