# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2025    Supplier Orders formatter
#
# ---------------------------------------------
from collections import defaultdict


def format_supplier_orders_to_history(orders, nmids):
    nmid_set = set(nmids or [])
    agg = defaultdict(lambda: {'ordersCount': 0, 'ordersSumRub': 0.0})

    for row in orders or []:
        try:
            nmid = int(row.get('nmId'))
        except Exception:
            continue

        if nmid_set and nmid not in nmid_set:
            continue

        if row.get('isCancel'):
            continue

        try:
            price = float(row.get('finishedPrice') or 0)
        except Exception:
            price = 0.0

        agg[nmid]['ordersCount'] += 1
        agg[nmid]['ordersSumRub'] += price

    result = []
    for nmid, metrics in agg.items():
        result.append({
            'nmID': nmid,
            'history': [
                {
                    'ordersCount': metrics['ordersCount'],
                    'ordersSumRub': round(metrics['ordersSumRub'], 2),
                }
            ]
        })

    return result

