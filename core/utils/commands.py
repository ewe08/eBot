from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='stats',
            description='Показать самых богатых',
        ),
        BotCommand(
            command='send',
            description='Передать свои токены(200 в день). '
                        'Чтобы отправить - ответь на сообщение того, '
                        'кому хочешь отправить командой /send {сумма}',
        ),
        BotCommand(
            command='help',
            description='Узнать правила бота',
        ),
        BotCommand(
            command='profile',
            description='Посмотреть свою статистику',
        ),
        BotCommand(
            command='ref',
            description='Получить реферальную ссылку. '
                        'Раз в месяц вы будете получать 10% токенов от всех рефералов',
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
