from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Профиль',
            ),
            KeyboardButton(
                text='Реферальная ссылка',
            ),
        ],
        [
            KeyboardButton(
                text='Помощь',
            )
        ]
    ],
    resize_keyboard=True,
)
