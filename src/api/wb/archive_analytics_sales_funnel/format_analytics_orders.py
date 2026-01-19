# ---------------------------------------------
# Program by @developer_telegrams
#
# Задача файла:
# - Преобразует ответ аналитики (sales-funnel/products/history)
#   в формат, совместимый с calculation_orders.py:
#   [{'nmID': <int>, 'history': [{'ordersCount': <int>, 'ordersSumRub': <float> }]}]
# ---------------------------------------------
from collections import defaultdict


def _extract_nmid(product):
    # Пробуем достать артикул (nmID) из блока "product"
    # Разные варианты ключей на случай изменений API
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


def format_analytics_orders_to_history(all_chunks_response, requested_nmids):
    # all_chunks_response: список ответов (каждый ответ — это список объектов {product, history})
    # requested_nmids: исходный список артикулов (для фильтрации результатов)
    #
    # Возвращает список словарей с ключами:
    # - nmID
    # - history: список с одним элементом { ordersCount, ordersSumRub }

    requested = set(requested_nmids or [])

    # Агрегируем данные по каждому nmID:
    # - ordersCount: сумма по всем дням за запрошенный период
    # - ordersSumRub: сумма по всем дням (переводим в float для совместимости)
    agg = defaultdict(lambda: {'ordersCount': 0, 'ordersSumRub': 0.0})

    # Проходим каждый ответ из пачек и каждый элемент внутри
    for chunk in all_chunks_response or []:
        for item in chunk or []:
            try:
                product = item.get('product') or {}
                history = item.get('history') or []
            except Exception:
                # Если структура не та, пропускаем
                continue

            # Достаём артикул из блока product
            nmid = _extract_nmid(product)
            if nmid is None:
                # Если nmID не нашли, не можем сопоставить — пропускаем
                continue

            # Фильтрация по исходному набору артикулов
            if requested and nmid not in requested:
                continue

            # Суммируем метрики по всем дням истории
            for day in history:
                try:
                    orders = int(day.get('orderCount') or 0)
                except Exception:
                    orders = 0
                try:
                    money = float(day.get('orderSum') or 0)
                except Exception:
                    money = 0.0

                agg[nmid]['ordersCount'] += orders
                agg[nmid]['ordersSumRub'] += money

    # Переводим агрегаты в целевой формат
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

