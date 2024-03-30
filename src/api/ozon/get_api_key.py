# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import OZON_API_KEY_LIST as API_KEY_LIST
from src.logger._logger import logger_msg


async def get_api_key(security):
    try:
        client_id = security[0]
    except Exception as es:
        msg = f'OZON get_api_key ошибка не могу получить client id "{es}"'

        await logger_msg(msg, push=True)

        return False, False

    try:
        api_key = security[1]
    except Exception as es:
        msg = f'OZON get_api_key ошибка не могу получить API ключ "{es}"'

        await logger_msg(msg, push=True)

        return False, False

    return client_id, api_key
