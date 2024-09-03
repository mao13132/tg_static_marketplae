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
from src.logger.logger_no_sync import logger_no_sync
from src.telegram.pinned_msg.pinned_msg import pinned_msg
from src.utils.generate_date import minus_days
from src.week_statistic.get_message_week.core_get_msg_week import core_get_msg_week
from src.week_statistic.get_week_data.start_get_week_data import StartGetWeekData


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

        get_data_from_server = await get_data_from_marketplace(self.BotDB, minus_days(1))

        # Получаю недельную статистику из таблиц
        get_week_data_from_sheet = await StartGetWeekData({'BotDB': self.BotDB}).start_get_week()

        ids_sql = []

        for manager in SEND_STATISTIC:

            personal_msg = await GetDate(self.BotDB, manager).get_msg()

            try:
                msg_send = await self.bot_start.bot.send_message(int(manager), personal_msg)
            except Exception as es:
                _error = f'Не могу отправить статистику менеджеру ({manager}) по расписанию "{es}"'

                await logger_msg(_error)

                continue

            await pinned_msg(self.bot_start.bot, manager, msg_send)

            # Week Statistic
            message_week = await core_get_msg_week(self.BotDB, manager)

            if not message_week:
                continue

            ids_sql = message_week['ids']

            message_week = message_week['msg']

            try:
                week_msg = await self.bot_start.bot.send_message(int(manager), message_week)
            except Exception as es:
                _error = f'Не могу отправить week статистику менеджеру ({manager}) по расписанию "{es}"'

                await logger_msg(_error)

                continue

            await pinned_msg(self.bot_start.bot, manager, week_msg)

        # Меняю статус на оправлено у sql строчек по week статистики
        if ids_sql:
            logger_no_sync(f'Отключаю: "{ids_sql}"')

            over_week_row_sql = [self.BotDB.over_week_row(row) for row in ids_sql]

        return True
