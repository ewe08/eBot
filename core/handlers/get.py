from aiogram.types import Message

from core.utils.dbconnect import Request
from core.handlers.basic import new_message


async def get_help(message: Message, request: Request):
    # await new_message(message, request)
    await message.answer('tut help')


async def get_profile(message: Message, request: Request):
    # await new_message(message, request)

    # [0id, 1user_id, 2chat_id, 3username, 4full_name, 5score,]
    # [6for_day, 7for_week, 8send_in_day, 9all_score]
    data = (await request.get_all_data(message.from_user.id, message.chat.id))[0]
    await message.answer(
        f'{data[4]}:\n'
        f'1. За этот месяц вы заработали: {data[5]}\n'
        f'2. За все время: {data[9]}\n'
        f'3. За сегодня(без учета переводов): {data[6]}\n'
        f'4. Абоба\n'
        f'5. За эту неделю вы активничали ровно {data[7]} дней\n'
    )


async def get_stats(message: Message, request: Request):
    # await new_message(message, request)
    data = await request.get_top_users(message.chat.id)
    response = ''
    i = 1
    for el in data:
        user_id, name, score = [x for x in el][0]
        response += f'{i}. {name} - {score} токен\n'
        i += 1
    await message.reply(response, parse_mode='Markdown')
