# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.week_statistic.get_message_week.get_all_text_msg import get_all_text_msg
from src.week_statistic.get_message_week.start_get_message_week import StartGetMessageWeek


async def core_get_msg_week(BotDB, user_id):
    settings_get_msg_week = {
        'BotDB': BotDB,
        'user_id': user_id,
    }

    data_week = await StartGetMessageWeek(settings_get_msg_week).start_get_message_week()

    if not data_week:
        return False

    msg_ = await get_all_text_msg(data_week)

    return_dict = {
        'msg': msg_,
        'ids': data_week['ids']
    }

    return return_dict



