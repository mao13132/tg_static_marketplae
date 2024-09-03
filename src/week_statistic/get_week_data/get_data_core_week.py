# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

import traceback
import sys

from settings import TARGET_DAY, ANALYST_DAY
from src.get_data._get_data import get_data_from_marketplace
from src.get_message.get_message_core import GetMessageCore
from src.logger._logger import logger_msg
from src.week_statistic.get_message_week.core_get_msg_week import core_get_msg_week
from src.week_statistic.get_week_data.start_get_week_data import StartGetWeekData


class GetDateWeek:
    def __init__(self, BotDB, user_id):

        self.BotDB = BotDB

        self.user_id = user_id

    async def get_msg(self):

        try:
            _message = await core_get_msg_week(self.BotDB, self.user_id)

            if not _message:
                return False

            _message = _message['msg']
        except Exception as es:

            await logger_msg(f"Ошибка при формировании week текста {es}\n"
                             f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

            return 'Ошибка формирования статистики'

        return _message

    async def get_statistic_msg_week(self):
        try:
            result_get_statistic = await StartGetWeekData({'BotDB': self.BotDB}).start_get_week()
        except Exception as es:

            await logger_msg(
                f"Ошибка при получение week статистики {es}\n"
                f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

            return 'Ошибка получения данных'

        _message = await self.get_msg()

        return _message
