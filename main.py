import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.scheduler.check_time import CheckTime
from src.telegram.bot_core import *
from src.telegram.callbacks.call_user import register_callbacks
from src.telegram.handlers.users import register_user
from src.telegram.state.states import register_state


def registration_all_handlers(dp):
    register_user(dp)


def registration_state(dp):
    register_state(dp)


def registration_calls(dp):
    register_callbacks(dp)


async def main():

    bot_start = Core()

    scheduler = AsyncIOScheduler()
    # await CheckTime(bot_start).check_scheduler()

    scheduler.add_job(CheckTime(bot_start).check_scheduler, 'interval', seconds=60, misfire_grace_time=300)

    registration_state(bot_start.dp)
    registration_all_handlers(bot_start.dp)
    registration_calls(bot_start.dp)

    scheduler.start()

    try:
        await bot_start.dp.start_polling()
    finally:
        await bot_start.dp.storage.close()
        await bot_start.dp.storage.wait_closed()
        await bot_start.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(f'Бот остановлен!')
