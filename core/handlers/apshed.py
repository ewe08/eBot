from aiogram import Bot

from core.settings import settings
from core.handlers.get import get_stats_response
from core.middlewares.dbmiddleware import Request
from core.utils.dbconnect import create_pool


async def collect_data_every_day(bot: Bot, admin_chat_id, chat_id):
    pool = await create_pool()
    request = Request(pool)
    message_in_day = (await request.get_day_data_in_chat(chat_id))
    for user in message_in_day:
        user = user[0]
        if user[2] >= 50:
            await request.update_week_data(user[0], user[1], 1)
        await request.set_day_data(user[0], user[1], 0)
    await bot.send_message(admin_chat_id, 'Бот работал целый день, не поломался')


async def collect_data_every_week(bot: Bot, admin_chat_id, chat_id):
    pool = await create_pool()
    request = Request(pool)

    message_in_week = await request.get_week_date_in_chat(chat_id)
    count = 0
    top = await get_stats_response(await request.get_top_week_users(settings.bots.work_chat_id))
    for user in message_in_week:
        user = user[0]
        referral = (await request.get_referral_id(user[0], chat_id))[0][0]
        if user[2] == 7:
            await request.update_score(user[0], user[1], 500)
            if referral:
                await request.update_referral_score(referral, chat_id, 50)
            count += 1
        await request.set_week_data(user[0], user[1], 0)
        await request.set_messages_for_week(user[0], user[1], 0)
    await bot.send_message(
        admin_chat_id,
        '#Отчет за неделю:\n'
        f'Заработали 500 - {count} человек\n'
        f'Топ недели: \n{top}'
    )


async def collect_data_every_month(bot: Bot, admin_chat_id, chat_id):
    pool = await create_pool()
    request = Request(pool)
    top = await get_stats_response(await request.get_top_users(settings.bots.work_chat_id))

    score_in_month = await request.get_score_in_chat(chat_id)
    for user in score_in_month:
        user_id, chat, score = user[0]
        referral_score = int((await request.get_referral_score(user_id, chat))[0][0])
        await request.update_score(user_id, chat, referral_score)
        await request.set_referral_score(user_id, chat, 0)
        await request.set_score(user_id, chat, 0)
    await bot.send_message(
        admin_chat_id,
        '#Отчет за месяц\n'
        f'Топ месяца: \n{top}'
    )
