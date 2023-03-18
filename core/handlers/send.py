from aiogram.types import Message

from core.handlers.basic import new_message
from core.utils.dbconnect import Request
from core.utils.exceptions import NotEnoughTokensError, ExceededDailyLimitError


async def send_score(message: Message, request: Request):
    await new_message(message, request)
    try:
        value = int(message.text.split()[1])
        limit = (await request.get_limit(message.from_user.id, message.chat.id))[0][0]
        score = (await request.get_score(message.from_user.id, message.chat.id))[0][0]

        if score < value:
            raise NotEnoughTokensError
        if limit + value > 200:
            raise ExceededDailyLimitError(limit)

        await request.update_limit(message.from_user.id, message.chat.id, value)
        await request.update_score(
            message.reply_to_message.from_user.id,
            message.chat.id,
            value,
        )
        await request.update_score(
            message.from_user.id,
            message.chat.id,
            -value,
        )
        await message.answer(
            f'{message.reply_to_message.from_user.full_name} успешно получил токены'
        )
    except ValueError:
        await message.reply('Аргумент должен быть натуральным числом')
    except AttributeError:
        await message.reply(
            'Ты должен ответить на сообщение пользователя, кому надо токены передать, дурик'
        )
    except NotEnoughTokensError:
        await message.reply(
            'Ты кого наебать хочешь? У тебя из имущества только жигуль батин. Куда столько бабла?'
            'Нет у тебя столько'
        )
    except ExceededDailyLimitError as e:
        await message.reply(
            f'Вы не можете отправить больше 200 в день. '
            f'Сегодня вы можете отправить максимум {200 - e.limit}'
        )
