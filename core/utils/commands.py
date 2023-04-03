from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats


async def set_commands_chat(bot: Bot):
    commands = [
        BotCommand(
            command='stats',
            description='Показать самых богатых',
        ),
        BotCommand(
            command='send',
            description='Передать свои токены(100 в день). '
                        'Чтобы отправить - ответь на сообщение того, '
                        'кому хочешь отправить командой /send {сумма}',
        ),
        BotCommand(
            command='balance',
            description='Посмотреть свое счастье.'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeAllGroupChats())


async def set_commands_user(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать чат',
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())
