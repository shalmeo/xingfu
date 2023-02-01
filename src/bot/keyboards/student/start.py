from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_start_markup():
    keyboard = [
        [
            KeyboardButton(text="Отзывы и результаты ❤️"),
            KeyboardButton(text="Игры на развитие ❤️"),
        ],
        [
            KeyboardButton(text="День открытых дверей ❤️"),
            KeyboardButton(text="Пригласить родителя ❤️"),
        ],
        [
            KeyboardButton(text="Личный кабинет ученика ❤️"),
            KeyboardButton(text="Пригласить ученика ❤️"),
        ],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
