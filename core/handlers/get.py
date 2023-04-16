import pathlib
from pathlib import Path

from aiogram.types import Message

from core.settings import settings
from core.utils.dbconnect import Request


async def get_help(message: Message):
    if message.chat.type == 'private':
        path = Path(pathlib.Path.cwd(), 'core', 'handlers', 'texts', 'help_text.txt')
        text = ''.join(
            open(path, encoding='UTF-8')
            .readlines())
        await message.answer(text, parse_mode='Markdown')
    else:
        await message.reply('Отправляйте эту команду в личные сообщения бота')


async def get_profile(message: Message, request: Request):
    # [0id, 1user_id, 2chat_id, 3username, 4full_name, 5score,]
    # [6for_day, 7for_week, 8send_in_day, 9all_score]
    if message.chat.type == 'private':
        data = (await request.get_all_data(message.from_user.id, settings.bots.work_chat_id))[0]
        await message.answer(
            f'{data[4]}:\n'
            f'1. За этот месяц вы заработали: {data[5]}\n'
            f'2. За все время: {data[9]}\n'
            f'3. За сегодня(без учета переводов): {data[6]}\n'
            f'5. За эту неделю вы активничали ровно {data[7]} дней (необходимо минимум 50 сообщений)\n'
        )
    else:
        await message.reply('Отправляйте эту команду в личные сообщения бота')


async def get_stats_response(data):
    response = ''
    i = 1
    for el in data:
        user_id, name, score = [x for x in el][0]
        response += f'{i}. {name} - {score} счастья\n'
        i += 1
    return response


async def get_stats(message: Message, request: Request):
    if message.chat.type != 'private':
        data = await request.get_top_users(message.chat.id)
        response = 'Самые активные за месяц:\n'
        response += await get_stats_response(data)
        await message.reply(response, parse_mode='Markdown')
    else:
        await message.reply('Этот метод используется для чата')


async def get_week_stats(message: Message, request: Request):
    if message.chat.type != 'private':
        data = await request.get_top_week_users(message.chat.id)
        response = 'Самые активные за неделю:\n'
        response += await get_stats_response(data)
        await message.reply(response, parse_mode='Markdown')
    else:
        await message.reply('Этот метод используется для чата')


async def get_balance(message: Message, request: Request):
    if message.chat.type != 'private':
        score = (await request.get_all_score(message.from_user.id, message.chat.id))[0][0]
        await message.reply(f'Ваш баланс: {score} счастья')
    else:
        await message.reply('Это команда для чата')
