# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import BRANDS_BY_DIRECTION, ACCESS, TARGET_DAY, ANALYST_DAY
from src.get_message.formate_row import formate_row
from src.get_message.sales_by_tags_block.generate_msg_by_tags import generate_msg_by_tags
from src.logger._logger import logger_msg


class TagsBlock:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.user_id = settings['user_id']

        self.security_brand = ACCESS[str(self.user_id)]

        self.data = {}

        self.total_order = 0

        self.total_money = 0

        self.total_order_yesterday = 0

        self.total_money_yesterday = 0

        self.access_user_brands = []

    async def plus_value(self, tags, _type, _value):
        if not _value:
            return False

        try:
            self.data[tags][_type] += _value
        except Exception as es:
            await logger_msg(f'tags_block: Не могу сложить число "{es}" "{tags}" "{_value}" "{_type}"')

            return False

        return True

    async def iter_brands_list(self, brands_list, tags):

        for brand in brands_list:
            orders_now = self.BotDB.get_all_marketplace_by_brands(brand, self.target_day, 'order')

            orders_now_count = orders_now[0]

            orders_now_money = orders_now[1]

            orders_yesterday = self.BotDB.get_all_marketplace_by_brands(brand, self.analyst_day, 'order')

            orders_yesterday_count = orders_yesterday[0]

            orders_yesterday_money = orders_yesterday[1]

            if orders_yesterday_count is None:
                orders_yesterday_count = 0

                message = f'Tags_block: нет данных за позавчерашний день "{brand}" по кол-ву заказов'

                await logger_msg(message, push=True)

            if orders_yesterday_money is None:
                orders_yesterday_money = 0

                message = f'Tags_block: нет данных за позавчерашний день "{brand}" по сумме заказов'

                await logger_msg(message, push=True)

            if orders_now_count is None:
                orders_now_count = 0

                message = f'Tags_block: нет данных за вчерашний день "{brand}" по кол-ву заказов'

                await logger_msg(message, push=True)

            if orders_now_money is None:
                orders_now_money = 0

                message = f'Tags_block: нет данных за вчерашний день "{brand}" по сумме заказов'

                await logger_msg(message, push=True)

            self.total_order += orders_now_count

            self.total_money += orders_now_money

            self.total_order_yesterday += orders_yesterday_count

            self.total_money_yesterday += orders_yesterday_money

            await self.plus_value(tags, 'total_orders', orders_now_count)

            await self.plus_value(tags, 'total_money', orders_now_money)

            await self.plus_value(tags, 'total_orders_yesterday', orders_yesterday_count)

            await self.plus_value(tags, 'total_money_yesterday', orders_yesterday_money)

        data_row_text = await formate_row(
            (self.data[tags]['total_orders'], self.data[tags]['total_money']),
            (self.data[tags]['total_orders_yesterday'], self.data[tags]['total_money_yesterday']))

        self.data[tags]['data_row_text'] = data_row_text

        return True

    def check_security_brand(self, brand_list):
        for brand in brand_list:
            if brand not in self.security_brand:
                return False

        return True

    async def iter_tags(self):
        self.data = {}

        self.total_order = 0

        self.total_money = 0

        self.total_order_yesterday = 0

        self.total_money_yesterday = 0

        for tags, brand_list in BRANDS_BY_DIRECTION.items():

            true_access = self.check_security_brand(brand_list)

            if not true_access:
                continue

            self.access_user_brands.extend(brand_list)

            maximal = self.BotDB.maximal_orders_all_brand_by_day('order', brand_list)

            exist_tags = self.data.get(tags, False)

            if not exist_tags:
                self.data[tags] = {}

                self.data[tags]['total_orders'] = 0

                self.data[tags]['total_orders_yesterday'] = 0

                self.data[tags]['total_money'] = 0

                self.data[tags]['total_money_yesterday'] = 0

                self.data[tags]['maximal'] = maximal

            res = await self.iter_brands_list(brand_list, tags)

        return self.data

    async def start_tags_block(self):
        data_one = await self.iter_tags()

        if not data_one:
            return ''

        total_data_row_text = await formate_row((self.total_order, self.total_money),
                                                (self.total_order_yesterday, self.total_money_yesterday))

        maximal_total = self.BotDB.maximal_orders_all_brand_by_day('order', self.access_user_brands)

        if maximal_total and self.total_order and self.total_money:
            if self.total_order >= maximal_total[0] or self.total_money >= maximal_total[1]:
                total_data_row_text = f"{total_data_row_text} 🍾🟢"

        message_tags = generate_msg_by_tags(data_one, total_data_row_text)

        return message_tags
