from aiogram.types import Message

from aiogram import Dispatcher

from settings import START_MESSAGE


async def start(message: Message):
    await message.bot.send_message(message.chat.id, START_MESSAGE)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
