from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link


async def get_ref(message: Message, bot: Bot):
    if message.chat.type == 'private':
        link = await create_start_link(
            bot=bot,
            payload=str(message.from_user.id),
            encode=True,
        )
        await message.answer(f'Ваша реф. ссылка {link}')
    else:
        await message.reply('Отправляйте эту команду в личные сообщения бота')
