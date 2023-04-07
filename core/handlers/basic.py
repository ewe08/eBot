from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from core.utils.dbconnect import Request
from core.keyboards.reply import reply_keyboard
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
        if await request.check_user(message.from_user.id, settings.bots.work_chat_id):
            await message.answer('С возвращением', reply_markup=reply_keyboard)
        else:
            start_command, *args = message.text.split()
            if args:
                referral_id = decode_payload(args[0])
                await add_user(message, settings.bots.work_chat_id, referral_id, request)
            await message.answer(
                'Вот ссылка на чат, Добро Пожаловать. ...',
                reply_markup=reply_keyboard,
            )
    else:
        await message.reply('Отправляйте эту команду в личные сообщения бота')


async def new_message(message: Message, request: Request):
    if message.chat.id != settings.bots.work_chat_id:
        return
    if not await request.check_user(message.from_user.id, message.chat.id):
        await request.add_data(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
            message.chat.id,
        )
    else:
        await request.update_user(
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
        await request.update_messages_for_week(message.from_user.id, message.chat.id, 1)
