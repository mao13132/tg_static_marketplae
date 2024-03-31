from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from settings import LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


class States(StatesGroup):
    set_time = State()


async def send_error(message):
    error_ = f'Вы ввели время не в верном формате. Попробуйте ещё раз.\n' \
             f'Формат 11:11'

    keyb = Admin_keyb().back()

    await Sendler_msg.send_msg_message(message, error_, keyb)

    return True


async def set_time(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    time_in = message.text

    try:
        hor, minute = time_in.split(':')
    except:

        await send_error(message)

        return False

    if not hor.isdigit() or not minute.isdigit():
        await send_error(message)

        return False

    if len(hor) > 2 or len(minute) > 2:
        await send_error(message)

        return False

    res_change_time = BotDB.edit_settings('time', time_in)

    keyb = Admin_keyb().start_keyb(time_in)

    await Sendler_msg().new_sendler_photo_message(message, LOGO, f'✅Время "{time_in}" успешно установленно', keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(set_time, state=States.set_time)
