import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from core.handlers.basic import get_start
from core.handlers.easter_egg import easter_egg
from core.settings import settings
from core.utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )

    bot = Bot(token=settings.bots.bot_token, parse_mode='')

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(easter_egg, F.text == 'Бот гей!')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
