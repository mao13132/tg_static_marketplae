# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.get_message.total_block.total_block import TotalBlock


class GetMessageCore:
    def __init__(self, settings):
        self.settings = settings

        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

    # async def get_orders_by_market_place(self, marketplace, brand):
    #
    #     orders_now = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.target_day, 'order')
    #
    #     orders_yesterday = self.BotDB.get_all_orders_by_brand(marketplace, brand, self.analyst_day, 'order')

    async def start_get_message(self):
        _message = ''

        total_block = await TotalBlock(self.settings).get_total_block()

        print()

        return _message
