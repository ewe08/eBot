from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from core.utils.dbconnect import Request


async def start_chat(message: Message, request: Request):
    start_command, *args = message.text.split()
    if args:
        payload = decode_payload(args[0])
    await message.answer(f"Ну тут типа привет тру ля ля вот ссылка на чат а твой батя гей. Чет такое")


async def new_message(message: Message, request: Request):
    if not await request.check_user(message.from_user.id, message.chat.id):
        await request.add_data(
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
            message.chat.id,
        )
    if len(message.text) >= 6:
        await request.update_score(message.from_user.id, message.chat.id, 1)
        await request.update_day_data(message.from_user.id, message.chat.id, 1)
