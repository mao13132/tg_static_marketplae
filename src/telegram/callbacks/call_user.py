from aiogram import Dispatcher

from src.get_data.get_data_core import GetDate
from src.logger._logger import logger_msg
from src.telegram.sendler.sendler import *

from src.telegram.bot_core import BotDB

from src.telegram.keyboard.keyboards import *


async def get_statistic(call: types.CallbackQuery):
    user_id = call.message.chat.id

    await Sendler_msg.log_client_call(call)

    send_msg = await Sendler_msg.send_msg_call(call, 'Начинаю получение данных. Ожидайте...', None)

    _msg = await GetDate(BotDB).get_statistic_msg()

    try:
        await call.message.bot.delete_message(user_id, send_msg.message_id)
    except:
        pass

    try:
        await call.message.bot.send_message(user_id, _msg)
    except Exception as es:
        error_ = f'Ошибка при отправке статистики "{es}"'

        await logger_msg(error_, push=True)

        await call.message.bot.send_message(user_id, error_)

        return False

    return True


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(get_statistic, text_contains='get_statistic')
