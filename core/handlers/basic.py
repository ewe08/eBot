from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from core.utils.dbconnect import Request
from core.settings import settings


async def add_user(message: Message, chat_id, referral_id, request: Request):
    await request.add_data_with_referral(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        chat_id,
        referral_id,
    )


async def start_chat(message: Message, request: Request):
    if message.chat.type == "private":
        start_command, *args = message.text.split()
        if args:
            referral_id = decode_payload(args[0])
            await add_user(message, settings.bots.work_chat_id, referral_id, request)
        await message.answer(
            ''
        )
    else:
        await message.reply('Отправляйте эту команду в личные сообщения бота')


async def new_message(message: Message, request: Request):
    if not await request.check_user(message.from_user.id, message.chat.id):
        await request.add_data(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
            message.chat.id,
        )
    if len(message.text) >= 6:
        referral = (await request.get_referral_id(message.from_user.id, message.chat.id))[0][0]
        if referral:
            await request.update_referral_score(referral, message.chat.id, 0.1)
        await request.update_score(message.from_user.id, message.chat.id, 1)
        await request.update_day_data(message.from_user.id, message.chat.id, 1)
