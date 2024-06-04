# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import OZON_API_KEY_LIST
from src.api.ozon.ozon_api_orders_profit import OzonApiOrdersProfit
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def get_statistic_orders_ozon(BotDB, target_day):
    print(f'\nНачинаю получать данные о заказах с OZON\n')

    ozon_core = OzonApiOrdersProfit()

    is_good = True

    for brand, security in OZON_API_KEY_LIST.items():

        access_false = filter_brand('ozon', brand)

        if access_false:
            continue

        data_statistic = await ozon_core.loop_get_orders_profit(
            'TG BOT', security, target_day, target_day)

        try:
            orders, profit = data_statistic
        except Exception as es:
            await logger_msg(f'get_data_core: Не могу распарсить ответ ozon с заказами и профитом "{es}"')

            continue

        sql_data = {
            'marketplace': 'ozon',
            'brand': brand,
            'type': 'order',
            'count': orders,
            'money': profit,
            'date': target_day,
        }

        res = BotDB.check_or_add_static(sql_data)

        if not res:
            is_good = False

        print(f'Обработал Ozon "{brand}"')

    print(f'Обработал все бренды по Ozon')

    return is_good
