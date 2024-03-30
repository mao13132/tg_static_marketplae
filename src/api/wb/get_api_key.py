# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import WB_API_KEY_LIST
from src.logger._logger import logger_msg


async def wb_get_api_key(name_ip, count):
    try:
        api_key_list = WB_API_KEY_LIST[name_ip]
    except Exception as es:
        msg = f'WB get_api_key ошибка, не могу получить API_KEY от {name_ip} "{es}"'

        await logger_msg(msg, push=True)

        return False

    try:
        api_key = api_key_list[count]
    except Exception as es:
        msg = f'WB get_api_key ошибка, распарсить ключ под номером {count} от {name_ip} "{es}"'

        await logger_msg(msg, push=True)

        return False

    return api_key
