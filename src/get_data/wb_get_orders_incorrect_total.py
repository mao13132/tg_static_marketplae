# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST
from src.api.wb.wb_api_orders_incorrect import WBApiOrders


async def wb_get_orders_incorrect_total(BotDB, target_day):
    print(f'Начинаю получать заказы с WB')

    wb_core = WBApiOrders()

    is_good = True

    for brand, security in WB_API_KEY_LIST.items():

        print(f'Начинаю получать заказы с {brand}')

        data_statistic = await wb_core.loop_get_orders(brand, target_day)

        if data_statistic:
            money = 0

            for order in data_statistic:
                money += order['priceWithDisc']

            orders = len(data_statistic)

            money = round(money, 2)
        else:
            money = 0

            orders = 0

        sql_data = {
            'marketplace': 'wb',
            'brand': brand,
            'type': 'order',
            'count': orders,
            'money': money,
            'date': target_day,
        }

        res = BotDB.check_or_add_static(sql_data)

        if not res:
            is_good = False

        print(f'Обработал заказы WB "{brand}"')

    print(f'Обработал все бренды по продажам WB')

    return is_good
