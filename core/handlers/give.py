from aiogram.types import Message

from core.settings import settings
from core.utils.dbconnect import Request
from core.utils.exceptions import NotValueError, SendingToBotError, TooManyArgumentsError


async def handle_input(message: Message, request: Request):
    try:
        if message.from_user.id != settings.bots.admin_id:
            await message.reply('Эта фича только для админа хихихи')
        else:
            args = message.text.split()
            if len(args) == 1:
                raise IndexError
            elif len(args) == 2:
                if message.reply_to_message.from_user.is_bot:
                    raise SendingToBotError
                user_id = message.reply_to_message.from_user.id
            elif len(args) == 3:
                user_id = (await (request.get_user_id_by_username(args[2][1:], message.chat.id)))[0][0]
            else:
                raise TooManyArgumentsError
            value = int(args[1])
            return value, user_id
    except NotValueError:
        await message.reply('Укажи, сколько')
    except SendingToBotError:
        await message.reply(
            'Вы не можете отправить счастье боту. Зачем?'
        )
    except IndexError:
        await message.reply(
            'Ты должен ответить на сообщение пользователя, либо написать его ник, кому надо счастье передать, дурик'
        )
    except TooManyArgumentsError:
        await message.reply('Чет много аргументов')


async def give_score(message: Message, request: Request):
    value, user_id = await handle_input(message, request)
    await request.update_score(
        user_id,
        message.chat.id,
        value,
    )
    await message.answer('Админ отправил вам милостыню')


async def remove_score(message: Message, request: Request):
    value, user_id = await handle_input(message, request)
    res = await request.get_score(user_id, message.chat.id)
    res = max(0, res[0][0] - value)
    await request.set_score(
        user_id,
        message.chat.id,
        res,
    )
    await message.answer('Админ наказал вас за грехи')
