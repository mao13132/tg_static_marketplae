# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
def generate_msg_total(data):
    _msg = f"Заказы WB: {data['wb']['order_text']}\n" \
           f"Заказы OZON: {data['ozon']['order_text']}\n" \
           f"Продажи WB: {data['wb']['sales_text']}\n" \
           f"Продажи OZON: {data['ozon']['sales_text']}\n" \
           f"Всего заказов: {data['total_orders_text']}\n" \
           f"Всего продаж: {data['total_sales_text']}"

    return _msg
