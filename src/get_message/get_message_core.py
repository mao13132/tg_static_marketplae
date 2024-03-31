# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.get_message.sales_by_brands.sales_block import SalesBlock
from src.get_message.total_block.total_block import TotalBlock


class GetMessageCore:
    def __init__(self, settings):
        self.settings = settings

        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

    async def start_get_message(self):
        _message = ''

        # total_block = await TotalBlock(self.settings).get_total_block()

        sales_block = await SalesBlock(self.settings).start_sales_block()

        print()

        return _message
