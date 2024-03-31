# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import MARKETPLACE
from src.get_message.formate_row import formate_row
from src.get_message.total_block.generate_msg_total import generate_msg_total


class TotalBlock:
    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.data = {}

    async def get_all_orders(self, marketplace):
        all_order_by_place_now = self.BotDB.get_all_orders_by_marketplace(marketplace, self.target_day, 'order')

        all_order_by_place_yesterday = self.BotDB.get_all_orders_by_marketplace(marketplace, self.analyst_day, 'order')

        data_row_text = await formate_row(all_order_by_place_now, all_order_by_place_yesterday)

        exist_place = self.data.get(marketplace, False)

        if not exist_place:
            self.data[marketplace] = {}

        self.data[marketplace]['orders_count'], self.data[marketplace]['orders_money'] = all_order_by_place_now

        self.data[marketplace]['order_text'] = data_row_text

        self.data['total_orders_count'] += self.data[marketplace]['orders_count']

        self.data['total_orders_money'] += self.data[marketplace]['orders_money']

        return True

    async def get_all_sales(self, marketplace):
        all_sales_by_place_now = self.BotDB.get_all_orders_by_marketplace(marketplace, self.target_day, 'sale')

        all_sales_by_place_yesterday = self.BotDB.get_all_orders_by_marketplace(marketplace, self.analyst_day, 'sale')

        data_row_text = await formate_row(all_sales_by_place_now, all_sales_by_place_yesterday)

        exist_place = self.data.get(marketplace, False)

        if not exist_place:
            self.data[marketplace] = {}

        self.data[marketplace]['sales_count'], self.data[marketplace]['sales_money'] = all_sales_by_place_now

        self.data[marketplace]['sales_text'] = data_row_text

        self.data['total_sales_count'] += self.data[marketplace]['sales_count']

        self.data['total_sales_money'] += self.data[marketplace]['sales_money']

        return True

    async def iter_marketplace(self):

        self.data['total_orders_count'] = 0

        self.data['total_orders_money'] = 0

        self.data['total_sales_count'] = 0

        self.data['total_sales_money'] = 0

        for marketplace in MARKETPLACE:
            res_orders = await self.get_all_orders(marketplace)

            res_money = await self.get_all_sales(marketplace)

        return True

    async def save_total_value(self):
        sql_data = {
            'marketplace': 'total',
            'brand': 'total',
            'type': 'sale',
            'count': self.data['total_sales_count'],
            'money': self.data['total_sales_money'],
            'date': self.target_day,
        }

        save_sales = self.BotDB.check_or_add_static(sql_data)

        sql_data = {
            'marketplace': 'total',
            'brand': 'total',
            'type': 'order',
            'count': self.data['total_orders_count'],
            'money': self.data['total_orders_money'],
            'date': self.target_day,
        }

        save_orders = self.BotDB.check_or_add_static(sql_data)

        return True

    async def get_total_yesterday(self):

        all_orders_by_place_yesterday = self.BotDB.get_all_orders_by_marketplace('total', self.analyst_day, 'order')

        order_row_text = await formate_row(
            (self.data['total_orders_count'], self.data['total_orders_money']), all_orders_by_place_yesterday)

        all_sales_by_sale_yesterday = self.BotDB.get_all_orders_by_marketplace('total', self.analyst_day, 'sale')

        sales_row_text = await formate_row(
            (self.data['total_sales_count'], self.data['total_sales_money']), all_sales_by_sale_yesterday)

        self.data['total_sales_text'] = order_row_text

        self.data['total_orders_text'] = sales_row_text

        return True

    async def get_total_block(self):
        result = await self.iter_marketplace()

        total_result = await self.save_total_value()

        total_yesterday = await self.get_total_yesterday()

        msg_total = generate_msg_total(self.data)

        return msg_total
