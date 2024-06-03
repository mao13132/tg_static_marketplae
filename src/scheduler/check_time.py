# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime

from settings import SEND_STATISTIC
from src.get_data._get_data import get_data_from_marketplace
from src.get_data.get_data_core import GetDate
from src.logger._logger import logger_msg
from src.utils.generate_date import minus_days


class CheckTime:
    def __init__(self, bot_start):
        self.BotDB = bot_start.BotDB

        self.bot_start = bot_start

    async def check_scheduler(self):
        sql_time = self.BotDB.get_settings_by_key('time')

        if not sql_time:
            return False

        hor, minute = sql_time.split(':')

        sql_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(hor), int(minute))

        now_time = datetime.now().replace(second=0, microsecond=0)

        if sql_time != now_time:
            return False

        get_data_from_db = await get_data_from_marketplace(self.BotDB, minus_days(1))

        for manager in SEND_STATISTIC:

            personal_msg = await GetDate(self.BotDB, manager).get_msg()

            try:
                await self.bot_start.bot.send_message(int(manager), personal_msg)
            except Exception as es:
                _error = f'Не могу отправить статистику менеджеру ({manager}) по расписанию "{es}"'

                await logger_msg(_error)

                continue

        return True
