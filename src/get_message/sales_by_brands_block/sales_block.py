# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import NAME_BRAND, MARKETPLACE
from src.get_message.formate_row import formate_row


class SalesBlock:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.msg = 'Заказы по брендам:\n'

    async def iter_market_place(self, brand):
        for marketplace in MARKETPLACE:
            orders_now = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.target_day, 'order')

            orders_yesterday = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.analyst_day, 'order')

            data_row_text = await formate_row(orders_now, orders_yesterday)

            self.msg += f'{brand} ({marketplace.upper()}): {data_row_text}\n'

        return True

    async def iter_brands(self):
        for key, brand in NAME_BRAND.items():
            result = await self.iter_market_place(brand)

        return True

    async def start_sales_block(self):
        result = await self.iter_brands()

        return self.msg
