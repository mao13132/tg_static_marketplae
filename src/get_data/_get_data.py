# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

from src.get_data.ozon.ozon_get_orders import get_statistic_orders_ozon
from src.get_data.ozon.ozon_get_sales import get_statistic_sales_ozon
from src.get_data.wb.wb_get_product_and_orders import wb_get_product_and_orders
from src.get_data.wb.wb_get_sales import wb_get_sales


async def get_data_from_marketplace(BotDB, target_day):
    res_orders_ozon = await get_statistic_orders_ozon(BotDB, target_day)

    res_sales_wb = await wb_get_sales(BotDB, target_day)

    res_sales_ozon = await get_statistic_sales_ozon(BotDB, target_day)

    res_orders_wb = await wb_get_product_and_orders(BotDB, target_day)

    print(f'\nЗакончил сбор данных с маркетплейсов\n')

    return True
