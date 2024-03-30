from aiogram import Dispatcher

from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *


async def adminka(call: types.CallbackQuery):

    keyb = Admin_keyb().start_keyb()

    text_admin = 'Админ панель:'

    await Sendler_msg().sendler_photo(call, r'media/admin.jpg', text_admin, keyb)

    await Sendler_msg.log_client_call(call)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(adminka, text_contains='adminka')
