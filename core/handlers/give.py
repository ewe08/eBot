from aiogram.types import Message

from core.settings import settings
from core.utils.dbconnect import Request
from core.utils.exceptions import NotValueError, SendingToBotError


async def give_score(message: Message, request: Request):
    try:
        if message.from_user.id != settings.bots.admin_id:
            await message.reply('Эта фича только для админа хихихи')
        else:
            args = message.text.split()
            if len(args) == 1:
                raise
            if message.reply_to_message.from_user.is_bot:
                raise SendingToBotError
            value = int(message.text.split()[1])
            await request.update_score(
                message.reply_to_message.from_user.id,
                message.chat.id,
                value,
            )
            await message.answer('Админ отправил вам милостыню')
    except NotValueError:
        await message.reply('Укажи, сколько')
    except SendingToBotError:
        await message.reply(
            'Вы не можете отправить токены боту. Зачем?'
        )
    except IndexError:
        await message.reply(
            'Ты должен ответить на сообщение пользователя, кому надо токены передать, дурик'
        )
