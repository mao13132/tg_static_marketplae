# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import NAME_BRAND, MARKETPLACE, ACCESS
from src.get_message.filter_brand.filter_brand import filter_brand
from src.get_message.formate_row import formate_row


class SalesBlock:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.user_id = settings['user_id']

        self.security_brand = ACCESS[str(self.user_id)]

        self.msg = '<b>Заказы по брендам:</b>\n'

    async def iter_market_place(self, brand):
        for marketplace in MARKETPLACE:

            stop_filter = filter_brand(marketplace, brand)

            if stop_filter:
                continue

            orders_now = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.target_day, 'order')

            orders_yesterday = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.analyst_day, 'order')

            data_row_text = await formate_row(orders_now, orders_yesterday)

            maximal_orders = self.BotDB.get_maximum_all_orders_by_brand(marketplace, brand, 'order')

            if maximal_orders and orders_now:
                if orders_now[0] >= maximal_orders[0] or orders_now[1] >= maximal_orders[1]:
                    data_row_text = f"{data_row_text} 🍾🟢"

            self.msg += f'{brand} ({marketplace.upper()}): {data_row_text}\n'

        return True

    async def iter_brands(self):
        for brand in self.security_brand:
            result = await self.iter_market_place(brand)

        return True

    async def start_sales_block(self):
        result = await self.iter_brands()

        return self.msg
