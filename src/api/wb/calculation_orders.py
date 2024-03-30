# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger._logger import logger_msg


async def calculation_orders(data_statistic, brand):
    count_orders = 0

    money = 0

    for order in data_statistic:
        try:
            for day in order['history']:
                count_orders += day['ordersCount']

                money += day['ordersSumRub']

        except Exception as es:
            await logger_msg(f'Ошибка при просчете заказов из ответа WB "{brand}" "{es}"', push=True)

            continue

    return count_orders, money
