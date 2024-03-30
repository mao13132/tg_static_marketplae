# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import logging

from src.logger.telegram.telegram_debug import Telegram


async def logger_msg(message, push=False):
    _msg = f'Logger: {message}'

    logging.error(_msg)

    print(_msg)

    if push:
        await Telegram().send_message(_msg)

    return True
