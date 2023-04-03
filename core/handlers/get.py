from aiogram import Bot
from aiogram.types import Message

from core.settings import settings
from core.utils.dbconnect import Request


async def get_help(message: Message):
    if message.chat.type == 'private':
        text = '''Правила просты:
    В чате присутствует внутренняя валюта, - это ничто иное как счастье 🤩
    1. Одно сообщение на 6 и более символов = 1 единица счастья
    2. Если вы каждый день на протяжении недели пишете по 50 и более сообщений, то в конце недели вам начисляется 500 единиц счастья, а ТОП 3 по общему количеству счастья на конец недели получают ???
    3. Статистика счатья обновляется каждую неделю (то есть отсчёт начинается заново), но на самом деле всё ваше счастье сохраняется и по итогу месяца результаты недель также складываются. Те, кто каждый день писал по 50 сообщений, но уже  в течении всего месяца - получают Х единиц счастья, А ТОП 3 по количеству счастья на конец месяца получают ???
    4. Месячная статистика тоже обновляется с каждым новым месяцем в 06:00 по МСК, но ВСЁ накопленное счастье суммируется и его потом можно будет использовать в нашем маркете
    5. В ТОП 3 можно участвовать даже если не пишешь каждый день, то есть награды за ежедневную активность в чате (1 пункт) и награды за место в ТОПЕ за неделю и месяц - это разные вещи и они суммируются.
    6. Общее количество счастья можно будет посмотреть по команде /profile в личном чате
    7. Реферальная система: раз в месяц вам будет начисляться 10% от счастья каждого приглашённого по вашей реферально ссылке друга, авторизированного в боте
    8. При технических неполадках, вопросах и прочем обращаться к @Amin01405 и @Eqake
    '''
        await message.answer(text)
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


async def get_stats(message: Message, bot: Bot, request: Request):
    if message.chat.type in ['group', 'supergroup']:
        data = await request.get_top_users(message.chat.id)
        response = 'Самые активные:\n'
        i = 1
        for el in data:
            user_id, name, score = [x for x in el][0]
            response += f'{i}. {name} - {score} счастья\n'
            i += 1
        await message.reply(response, parse_mode='Markdown')
    else:
        await message.reply('Этот метод используется для чата')