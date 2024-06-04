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


class GetDate:
    def __init__(self, BotDB, user_id):
        self.target_day = TARGET_DAY

        self.analyst_day = ANALYST_DAY

        self.BotDB = BotDB

        self.user_id = user_id

    async def get_msg(self):
        message_settings = {
            'BotDB': self.BotDB,
            'target_day': self.target_day,
            'analyst_day': self.analyst_day,
            'user_id': self.user_id,
        }

        try:
            _message = await GetMessageCore(message_settings).start_get_message()
        except Exception as es:

            await logger_msg(f"Ошибка при формировании текста {es}\n"
                             f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

            return 'Ошибка формирования статистики'

        return _message

    async def get_statistic_msg(self, _write=False):
        try:
            result_get_statistic = await get_data_from_marketplace(self.BotDB, self.target_day)
        except Exception as es:

            if _write:
                _write.status = False

            await logger_msg(
                f"Ошибка при получение статистики {es}\n"
                f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}")

            return 'Ошибка получения данных'

        _message = await self.get_msg()

        if _write:
            _write.status = False

        return _message
