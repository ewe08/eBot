from aiogram import Bot

from core.middlewares.dbmiddleware import Request


async def collect_data_every_day(chat_id, request: Request):
    message_in_day = await request.get_data_day_in_chat(chat_id)
    for user in message_in_day:
        if user[1] >= 50:
            await request.update_data_day_by_id(user[0], 0)
            await request.update_data_week_by_id(user[0], 1)


async def collect_data_every_week(chat_id, request: Request):
    await collect_data_every_day(chat_id, request)

    message_in_week = await request.get_data_week_in_chat(chat_id)
    for user in message_in_week:
        if user[1] == 7:
            await request.update_data_week_by_id(user[0], 0)
            await request.update


async def collect_data_every_month(bot: Bot, request: Request):
    pass
