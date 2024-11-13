# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger.logger_no_sync import logger_no_sync
from src.logger.telegram.telegram_debug_no_sync import SendlerOneCreate


async def clear_float(value):
    good_value = ''

    for word in str(value):

        if word == ',':
            good_value += '.'

            continue

        if word == '-':
            good_value += word

            continue

        if word.isdigit():
            good_value += word

    try:
        good_value = float(good_value)
    except Exception as es:
        error_ = f'Не могу конвертировать значение "{value}" из sheet в float "{es}"'

        logger_no_sync(error_)

        SendlerOneCreate('').save_text(error_)

        return 0

    return good_value


async def clear_int(value):
    good_value = ''

    for word in str(value):
        if word.isdigit():
            good_value += word

    try:
        good_value = int(good_value)
    except Exception as es:
        error_ = f'Не могу конвертировать значение "{value}" в int из sheet в float "{es}"'

        logger_no_sync(error_)

        SendlerOneCreate('').save_text(error_)

        return 0

    return good_value
