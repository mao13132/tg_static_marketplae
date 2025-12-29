# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST
from src.api.wb.calculation_orders import calculation_orders
from src.api.wb.wb_api_supplier_orders import WBApiSupplierOrders
from src.api.wb.wb_api_get_products import WBApiGetProducts
from src.api.wb.wb_orders_formatter import format_supplier_orders_to_history
from src.get_message.filter_brand.filter_brand import filter_brand
from src.logger._logger import logger_msg


async def wb_get_product_and_orders(BotDB, target_day):
    print(f'\nНачинаю получать заказы с WB\n')

    wb_core = WBApiSupplierOrders()

    is_good = True

    for brand, security in WB_API_KEY_LIST.items():

        access_false = filter_brand('wb', brand)

        if access_false:
            continue

        print(f'Начинаю получать продукты с {brand}')

        products = await WBApiGetProducts().loop_get_products(brand)

        if not products:
            await logger_msg(f'Не могу получить список продуктов "{brand}"', push=True)

            continue

        article_list = [product['nmID'] for product in products]

        print(f'Начинаю получать заказы с {brand}')
        orders_raw = await wb_core.loop_get_orders_for_date(brand, target_day)
        data_statistic = format_supplier_orders_to_history(orders_raw, article_list)

        if data_statistic:

            orders, money = await calculation_orders(data_statistic, brand)

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
