from aiogram.types import Message

from aiogram import Dispatcher

from settings import START_MESSAGE, ADMIN, LOGO, SEND_STATISTIC
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


async def start(message: Message):
    await Sendler_msg.log_client_message(message)

    user_id = message.chat.id

    if str(user_id) not in ADMIN and str(user_id) not in SEND_STATISTIC:
        await Sendler_msg().new_sendler_photo_message(message, LOGO, f'В доступе отказано!', None)

        return False

    current_time = BotDB.get_settings_by_key('time')

    if not current_time:
        current_time = 'Не указанно'

    keyb = Admin_keyb().start_keyb(current_time)

    await Sendler_msg().new_sendler_photo_message(message, LOGO, START_MESSAGE, keyb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
