from aiogram.types import Message

from aiogram import Dispatcher

from settings import START_MESSAGE, ADMIN, LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg


async def start(message: Message):
    user_id = message.chat.id

    if str(user_id) not in ADMIN:

        return False

    keyb = Admin_keyb().start_keyb()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, START_MESSAGE, keyb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
