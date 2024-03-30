# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.get_data.ozon_get_statistic import get_statistic_ozon
from src.utils.generate_date import minus_days


class GetDate:
    def __init__(self, bot_start):
        self.target_day = minus_days(2)

        self.analyst_day = minus_days(2)

        self.BotDB = bot_start.BotDB

    async def start_get_statistic(self):
        res_ozon = await get_statistic_ozon(self.BotDB, self.target_day)

        print()
