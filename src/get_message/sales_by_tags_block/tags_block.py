# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import BRANDS_BY_DIRECTION
from src.get_message.formate_row import formate_row
from src.get_message.sales_by_tags_block.generate_msg_by_tags import generate_msg_by_tags
from src.logger._logger import logger_msg


class TagsBlock:

    def __init__(self, settings):
        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.data = {}

    async def plus_value(self, tags, _type, _value):
        try:
            self.data[tags][_type] += _value
        except Exception as es:
            await logger_msg(f'tags_block: Не могу сложить число "{es}" "{tags}" "{_value}" "{_type}"')

            return False

        return True

    async def iter_brands_list(self, brands_list, tags):
        for brand in brands_list:
            orders_now = self.BotDB.get_all_marketplace_by_brands(brand, self.target_day, 'order')

            orders_yesterday = self.BotDB.get_all_marketplace_by_brands(brand, self.analyst_day, 'order')

            await self.plus_value(tags, 'total_orders', orders_now[0])

            await self.plus_value(tags, 'total_money', orders_now[1])

            await self.plus_value(tags, 'total_orders_yesterday', orders_yesterday[0])

            await self.plus_value(tags, 'total_money_yesterday', orders_yesterday[1])

        data_row_text = await formate_row(
            (self.data[tags]['total_orders'], self.data[tags]['total_money']),
            (self.data[tags]['total_orders_yesterday'], self.data[tags]['total_money_yesterday']))

        self.data[tags]['data_row_text'] = data_row_text

        return True

    async def iter_tags(self):
        for tags, brand_list in BRANDS_BY_DIRECTION.items():

            exist_tags = self.data.get(tags, False)

            if not exist_tags:
                self.data[tags] = {}

                self.data[tags]['total_orders'] = 0

                self.data[tags]['total_orders_yesterday'] = 0

                self.data[tags]['total_money'] = 0

                self.data[tags]['total_money_yesterday'] = 0

            res = await self.iter_brands_list(brand_list, tags)

        return True

    async def start_tags_block(self):
        result = await self.iter_tags()

        message_tags = generate_msg_by_tags(self.data)

        return message_tags
