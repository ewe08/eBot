from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link, decode_payload


async def get_ref(message: Message, bot: Bot):
    link = await create_start_link(
        bot=bot,
        payload=str(message.from_user.id),
        encode=True,
    )
    await message.answer(f"Ваша реф. ссылка {link}")
