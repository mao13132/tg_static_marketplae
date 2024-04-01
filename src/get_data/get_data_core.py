# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

import traceback
import sys

from src.get_data.ozon.ozon_get_orders import get_statistic_orders_ozon
from src.get_data.ozon.ozon_get_sales import get_statistic_sales_ozon
from src.get_data.wb.wb_get_product_and_orders import wb_get_product_and_orders
from src.get_data.wb.wb_get_sales import wb_get_sales
from src.get_message.get_message_core import GetMessageCore
from src.logger._logger import logger_msg
from src.utils.generate_date import minus_days


class GetDate:
    def __init__(self, BotDB):
        self.target_day = minus_days(1)

        self.analyst_day = minus_days(2)

        self.BotDB = BotDB

    async def get_data_from_marketplace(self):
        res_orders_ozon = await get_statistic_orders_ozon(self.BotDB, self.target_day)

        res_sales_wb = await wb_get_sales(self.BotDB, self.target_day)

        res_sales_ozon = await get_statistic_sales_ozon(self.BotDB, self.target_day)

        res_orders_wb = await wb_get_product_and_orders(self.BotDB, self.target_day)

        print(f'\nЗакончил сбор данных с маркетплейсов\n')

        return True

    async def get_statistic_msg(self):
        try:
            result_get_statistic = await self.get_data_from_marketplace()
        except Exception as es:
            await logger_msg(f"Ошибка при получение статистики {es}\n"
                             f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

        message_settings = {
            'BotDB': self.BotDB,
            'target_day': self.target_day,
            'analyst_day': self.analyst_day,
        }

        try:
            _message = await GetMessageCore(message_settings).start_get_message()
        except Exception as es:

            await logger_msg(f"Ошибка при формировании текста {es}\n"
                             f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

            return 'Ошибка формирования статистики'

        return _message
