import asyncio

from aiogram.types import Message, ChatActions


class Write:
    def __init__(self):
        self.status = True

    async def write(self, message: Message):
        while self.status:
            try:
                await message.bot.send_chat_action(message.chat.id, ChatActions.TYPING)
            except:
                pass
            await asyncio.sleep(1)
