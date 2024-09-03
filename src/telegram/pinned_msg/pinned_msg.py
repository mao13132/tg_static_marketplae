# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.logger.logger_no_sync import logger_no_sync


async def pinned_msg(bot, id_user, target_message):
    try:
        await bot.pin_chat_message(chat_id=int(id_user),
                                           message_id=target_message['message_id'])
    except Exception as es:
        logger_no_sync(f'Не могу запинить сообщение "{es}" user "{id_user}"')

        return False

    return True
