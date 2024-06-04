# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import OZON_API_KEY_LIST
from src.api.ozon.ozon_api_sales import OzonApiSales
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def get_statistic_sales_ozon(BotDB, target_day):
    print(f'\nНачинаю получать данные о продажах с OZON\n')

    ozon_core = OzonApiSales()

    is_good = True

    for brand, security in OZON_API_KEY_LIST.items():

        access_false = filter_brand('ozon', brand)

        if access_false:
            continue

        data_statistic = await ozon_core.loop_get_sales_ozon(
            brand, security, target_day)

        if data_statistic:

            sales = len(data_statistic)

            money = 0

            for sale in data_statistic:
                money += sale['accruals_for_sale']

        else:
            money = 0

            sales = 0

        sql_data = {
            'marketplace': 'ozon',
            'brand': brand,
            'type': 'sale',
            'count': sales,
            'money': money,
            'date': target_day,
        }

        res = BotDB.check_or_add_static(sql_data)

        if not res:
            is_good = False

        print(f'Обработал Ozon "{brand}"')

    print(f'Обработал все бренды по Ozon')

    return is_good
