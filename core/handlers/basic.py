from aiogram.types import Message

from core.utils.dbconnect import Request


async def new_message(message: Message, request: Request):
    if len(message.text) >= 6:
        if not await request.check_user(message.from_user.id, message.chat.id):
            await request.add_data(
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name,
                message.chat.id,
            )
        await request.update_data_score(message.from_user.id, message.chat.id, 1)
        await request.update_data_day(message.from_user.id, message.chat.id, 1)
