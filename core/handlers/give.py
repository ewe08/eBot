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
            'Вы не можете отправить счастье боту. Зачем?'
        )
    except IndexError:
        await message.reply(
            'Ты должен ответить на сообщение пользователя, кому надо счастье передать, дурик'
        )


async def remove_score(message: Message, request: Request):
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
            res = await request.get_score(message.reply_to_message.from_user.id, message.chat.id)
            res = max(0, res[0][0] - value)
            await request.set_score(
                message.reply_to_message.from_user.id,
                message.chat.id,
                res,
            )
            await message.answer('Админ наказал вас за грехи')
    except NotValueError:
        await message.reply('Укажи, сколько')
    except SendingToBotError:
        await message.reply(
            'Вы не можете отправить счастье боту. Зачем?'
        )
    except IndexError:
        await message.reply(
            'Ты должен ответить на сообщение пользователя, кому надо счастье передать, дурик'
        )
