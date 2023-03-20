import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from core.handlers.apshed import collect_data_every_day, collect_data_every_week
from core.handlers.apshed import collect_data_every_month
from core.handlers.basic import new_message, start_chat
from core.handlers.get import get_stats, get_help, get_profile
from core.handlers.send import send_score
from core.handlers.ref import get_ref
from core.middlewares.dbmiddleware import DbSession
from core.settings import settings
from core.utils.commands import set_commands
from core.utils.dbconnect import create_pool


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    pass
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pull_connect = await create_pool()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        collect_data_every_day,
        trigger='cron',
        hour=18,
        kwargs={
            'chat_id': settings.bots.work_chat_id,
        }
    )
    scheduler.add_job(
        collect_data_every_week,
        trigger='cron',
        day_of_week='mon',
        hour=18,
        kwargs={
            'chat_id': settings.bots.work_chat_id,
        }
    )
    scheduler.add_job(
        collect_data_every_month,
        trigger='cron',
        day=1,
        hour=18,
        kwargs={
            'bot': bot,
            'admin_chat_id': settings.bots.admin_chat_id,
            'chat_id': settings.bots.work_chat_id,
        }
    )
    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pull_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_stats, Command(commands=['stats']))
    dp.message.register(get_help, Command(commands=['help']))
    dp.message.register(get_profile, Command(commands=['profile']))
    dp.message.register(send_score, Command(commands=['send']))
    dp.message.register(get_ref, Command(commands=['ref']))
    dp.message.register(start_chat, Command(commands=['start']))

    dp.message.register(new_message)

    try:
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
