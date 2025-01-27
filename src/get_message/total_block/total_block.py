# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import MARKETPLACE, ACCESS, NAME_BRAND, TARGET_DAY, ANALYST_DAY
from src.get_message.check_is_none import check_is_none_from_tuple
from src.get_message.formate_row import formate_row
from src.get_message.total_block.generate_msg_total import generate_msg_total, generate_msg_total_from_admin
from src.utils.generate_date import minus_days


class TotalBlock:
    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.user_id = settings['user_id']

        self.security_brand = ACCESS[str(self.user_id)]

        self.data = {}

    async def get_all_orders(self, marketplace, brand_list):

        all_order_by_place_now = self.BotDB.new_get_all_orders_by_marketplace(
            marketplace, self.target_day, 'order', brand_list)

        all_order_by_place_now = check_is_none_from_tuple(all_order_by_place_now)

        all_order_by_place_yesterday = self.BotDB.new_get_all_orders_by_marketplace(
            marketplace, self.analyst_day, 'order', brand_list)

        all_order_by_place_yesterday = check_is_none_from_tuple(all_order_by_place_yesterday)

        data_row_text = await formate_row(all_order_by_place_now, all_order_by_place_yesterday)

        # Проверка на максимальные значения первый блок
        maximal_summ = self.BotDB.maximal_orders_all_marketplaces_by_day(marketplace, 'order', brand_list)

        if maximal_summ and all_order_by_place_now:
            if all_order_by_place_now[0] > maximal_summ[0] or all_order_by_place_now[1] > maximal_summ[1]:
                data_row_text = f"{data_row_text} 🍾🟢"

        exist_place = self.data.get(marketplace, False)

        if not exist_place:
            self.data[marketplace] = {}

        self.data[marketplace]['orders_count'], self.data[marketplace]['orders_money'] = all_order_by_place_now

        self.data[marketplace]['order_text'] = data_row_text

        self.data['total_orders_count'] += self.data[marketplace]['orders_count']

        self.data['total_orders_money'] += self.data[marketplace]['orders_money']

        return True

    async def get_all_sales(self, marketplace, brand_list):
        all_sales_by_place_now = self.BotDB.new_get_all_orders_by_marketplace(
            marketplace, self.target_day, 'sale', brand_list)

        all_sales_by_place_now = check_is_none_from_tuple(all_sales_by_place_now)

        all_sales_by_place_yesterday = self.BotDB.new_get_all_orders_by_marketplace(
            marketplace, self.analyst_day, 'sale', brand_list)

        all_sales_by_place_yesterday = check_is_none_from_tuple(all_sales_by_place_yesterday)

        data_row_text = await formate_row(all_sales_by_place_now, all_sales_by_place_yesterday)

        exist_place = self.data.get(marketplace, False)

        if not exist_place:
            self.data[marketplace] = {}

        self.data[marketplace]['sales_count'], self.data[marketplace]['sales_money'] = all_sales_by_place_now

        self.data[marketplace]['sales_text'] = data_row_text

        self.data['total_sales_count'] += self.data[marketplace]['sales_count']

        self.data['total_sales_money'] += self.data[marketplace]['sales_money']

        return True

    async def iter_marketplace(self, brand_list):

        self.data = {}

        self.data['total_orders_count'] = 0

        self.data['total_orders_money'] = 0

        self.data['total_sales_count'] = 0

        self.data['total_sales_money'] = 0

        for marketplace in MARKETPLACE:
            res_orders = await self.get_all_orders(marketplace, brand_list)

            res_money = await self.get_all_sales(marketplace, brand_list)

        return self.data

    async def get_total_yesterday(self, total_sum_one, total_sum_two):

        all_orders_by_place_yesterday = (total_sum_two['total_orders_count'], total_sum_two['total_orders_money'])

        order_row_text = await formate_row(
            (total_sum_one['total_orders_count'], total_sum_one['total_orders_money']), all_orders_by_place_yesterday)

        all_sales_by_sale_yesterday = (total_sum_two['total_sales_count'], total_sum_two['total_sales_money'])

        sales_row_text = await formate_row(
            (total_sum_one['total_sales_count'], total_sum_one['total_sales_money']), all_sales_by_sale_yesterday)

        total_sum_one['total_sales_text'] = sales_row_text

        total_sum_one['total_orders_text'] = order_row_text

        return total_sum_one

    async def get_start_data(self, brand_list):

        self.target_day = TARGET_DAY

        self.analyst_day = ANALYST_DAY

        total_data_one = await self.iter_marketplace(brand_list)

        self.target_day = minus_days(2)

        self.analyst_day = minus_days(3)

        total_data_two = await self.iter_marketplace(brand_list)

        total_data = await self.get_total_yesterday(total_data_one, total_data_two)

        return total_data

    async def get_total_block(self):
        brand_list = [x for x in ACCESS[str(self.user_id)]]

        total_data = await self.get_start_data(brand_list)

        msg_total = generate_msg_total(total_data)

        return msg_total

    async def get_total_block_from_admin(self):
        brand_list = [x for x in ACCESS[str(self.user_id)]]

        no_zavod_bit_zhim = [x for x in brand_list if x != NAME_BRAND[10]]

        total_data = await self.get_start_data(brand_list)

        no_zavod_data = await self.get_start_data(no_zavod_bit_zhim)

        total_sale_no_zavod = no_zavod_data['total_orders_text']

        msg_total = generate_msg_total_from_admin(total_data, total_sale_no_zavod)

        return msg_total
