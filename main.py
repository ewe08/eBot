import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from core.handlers.apshed import collect_data_every_day
from core.handlers.apshed import collect_data_every_week
from core.handlers.apshed import collect_data_every_month
from core.handlers.basic import new_message, start_chat
from core.handlers.get import get_stats, get_help, get_profile
from core.handlers.send import send_score
from core.handlers.ref import get_ref
from core.middlewares.dbmiddleware import DbSession
from core.settings import settings
from core.utils.commands import set_commands_chat, set_commands_user
from core.utils.dbconnect import create_pool


async def start_bot(bot: Bot):
    await set_commands_chat(bot)
    await set_commands_user(bot)


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    await bot.delete_webhook(drop_pending_updates=True)

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

    dp.message.register(start_chat, Command(commands=['start']))
    dp.message.register(get_stats, Command(commands=['stats']))
    dp.message.register(send_score, Command(commands=['send']))
    dp.message.register(get_help, F.text == 'Помощь')
    dp.message.register(get_profile, F.text == 'Профиль')
    dp.message.register(get_ref, F.text == 'Реферальная ссылка')

    dp.message.register(new_message)

    try:
        scheduler.start()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
