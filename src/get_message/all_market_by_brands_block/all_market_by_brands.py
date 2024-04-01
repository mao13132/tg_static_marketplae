# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import NAME_BRAND
from src.get_message.formate_row import formate_row


class AllMarketByBrands:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.msg = '<b>Общие по брендам:</b>\n'

    async def iter_brands(self):
        for key, brand in NAME_BRAND.items():

            orders_now = self.BotDB.get_all_marketplace_by_brands(brand, self.target_day, 'order')

            orders_yesterday = self.BotDB.get_all_marketplace_by_brands(brand, self.analyst_day, 'order')

            data_row_text = await formate_row(orders_now, orders_yesterday)

            self.msg += f'{brand}: {data_row_text}\n'

        return True

    async def start_brands_block(self):
        result = await self.iter_brands()

        return self.msg
