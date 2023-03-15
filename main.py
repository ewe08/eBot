import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from core.handlers.basic import new_message
from core.handlers.get import get_stats, get_help, get_profile
from core.handlers.send import send_score
from core.middlewares.dbmiddleware import DbSession
from core.settings import settings
from core.utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    # await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    pass
    # await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.databases.user,
        password=settings.databases.password,
        database=settings.databases.database,
        host=settings.databases.host,
        port=settings.databases.port,
        command_timeout=settings.databases.command_timeout,
    )


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pull_connect = await create_pool()

    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pull_connect))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_stats, Command(commands=['stats']))
    dp.message.register(get_help, Command(commands=['help']))
    dp.message.register(get_profile, Command(commands=['profile']))
    dp.message.register(send_score, Command(commands=['send']))
    dp.message.register(new_message)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
