from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


class States(StatesGroup):
    test = State()

async def test(message: Message, state: FSMContext):

    try:
        await message.bot.send_message(message.chat.id, 'Ответы приняты. Опрос окончен')
    except Exception as es:
        print(f'Ошибка {es}')

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(test, state=States.test)
