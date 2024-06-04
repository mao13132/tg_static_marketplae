# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST
from src.api.wb.wb_api_sales import WBApiSales
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def wb_get_sales(BotDB, target_day):
    print(f'\nНачинаю получать продажи с WB\n')

    wb_core = WBApiSales()

    is_good = True

    for brand, security in WB_API_KEY_LIST.items():

        access_false = filter_brand('wb', brand)

        if access_false:
            continue

        print(f'Начинаю получать продажи с {brand}')

        data_statistic = await wb_core.loop_get_sales(brand, target_day)

        if data_statistic:
            money = 0

            for sale in data_statistic:
                money += sale['forPay']

            sales = len(data_statistic)

            money = round(money, 2)
        else:
            money = 0

            sales = 0

        sql_data = {
            'marketplace': 'wb',
            'brand': brand,
            'type': 'sale',
            'count': sales,
            'money': money,
            'date': target_day,
        }

        res = BotDB.check_or_add_static(sql_data)

        if not res:
            is_good = False

        print(f'Обработал продажи WB "{brand}"')

    print(f'Обработал все бренды по продажам WB')

    return is_good
