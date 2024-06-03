# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import ACCESS, ADMIN
from src.get_message.all_market_by_brands_block.all_market_by_brands import AllMarketByBrands
from src.get_message.sales_by_brands_block.sales_block import SalesBlock
from src.get_message.sales_by_tags_block.tags_block import TagsBlock
from src.get_message.total_block.total_block import TotalBlock


class GetMessageCore:
    def __init__(self, settings):
        self.settings = settings

        self.BotDB = settings['BotDB']

        self.target_day = settings['target_day']

        self.analyst_day = settings['analyst_day']

        self.user_id = settings['user_id']

    async def start_get_message(self):
        print(f'\nНачинаю формировать сообщение с данными\n')

        if str(self.user_id) in ADMIN:
            total_block = await TotalBlock(self.settings).get_total_block_from_admin()
        else:
            total_block = await TotalBlock(self.settings).get_total_block()

        sales_block = await SalesBlock(self.settings).start_sales_block()

        # brands_block = await AllMarketByBrands(self.settings).start_brands_block()

        tags_block = await TagsBlock(self.settings).start_tags_block()

        main_msg = f'<b>Данные от {self.target_day}</b>\n\n' \
                   f'{total_block}\n\n{sales_block}\n{tags_block}'
        # f'{total_block}\n\n{sales_block}\n{brands_block}\n{tags_block}'

        return main_msg
