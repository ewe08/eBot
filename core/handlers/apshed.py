from aiogram import Bot

from core.middlewares.dbmiddleware import Request
from core.utils.dbconnect import create_pool


async def collect_data_every_day(chat_id):
    pool = await create_pool()
    request = Request(pool)
    message_in_day = (await request.get_day_data_in_chat(chat_id))
    for user in message_in_day:
        user = user[0]
        if user[2] >= 50:
            await request.update_week_data(user[0], user[1], 1)
        await request.set_day_data(user[0], user[1], 0)


async def collect_data_every_week(chat_id):
    pool = await create_pool()
    request = Request(pool)

    message_in_week = await request.get_week_date_in_chat(chat_id)
    for user in message_in_week:
        user = user[0]
        if user[2] == 7:
            await request.update_score(user[0], user[1], 500)
        await request.set_week_data(user[0], user[1], 0)


async def collect_data_every_month(bot: Bot, admin_chat_id, chat_id):
    pool = await create_pool()
    request = Request(pool)
    score_in_month = await request.get_score_in_chat(chat_id)
    for user in score_in_month:
        user = user[0]
        await request.set_score(user[0], user[1], 0)
    await bot.send_message(admin_chat_id, '#Отчет за месяц')