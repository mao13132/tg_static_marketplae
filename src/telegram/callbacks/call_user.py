from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from src.get_data.get_data_core import GetDate
from src.logger._logger import logger_msg
from src.telegram.handlers.users import start
from src.telegram.sendler.sendler import *

from src.telegram.bot_core import BotDB

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States


async def get_statistic(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    user_id = call.message.chat.id

    send_msg = await Sendler_msg.send_msg_call(call, 'Начинаю получение данных. Примерно время ожидания 2 минуты. '
                                                     'Ожидайте...', None)

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


async def change_time(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    user_id = call.message.chat.id

    keyb = Admin_keyb().back()

    await Sendler_msg.send_msg_call(call, '⚠️Введите в какое время необходимо присылать отчёт\n'
                                          'Формат 11:00 или 11:11', keyb)

    await States.set_time.set()

    return True


async def back(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

    current_time = BotDB.get_settings_by_key('time')

    if not current_time:
        current_time = 'Не указанно'

    keyb = Admin_keyb().start_keyb(current_time)

    await Sendler_msg().sendler_photo_call(call, LOGO, START_MESSAGE, keyb)

    return True


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(back, text='back', state='*')

    dp.register_callback_query_handler(get_statistic, text_contains='get_statistic')

    dp.register_callback_query_handler(change_time, text_contains='change_time')
