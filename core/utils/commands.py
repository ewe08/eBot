from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='stats',
            description='Показать самых богатых',
        ),
        BotCommand(
            command='give',
            description='Передать свои токены(200 в день)',
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
