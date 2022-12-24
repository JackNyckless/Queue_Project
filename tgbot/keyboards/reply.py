from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Си"),
            KeyboardButton(text="Тисд"),
            KeyboardButton(text="Птп"),
        ],
        [
            KeyboardButton(text="Посмотреть свои позиции"),
        ],
        [
            KeyboardButton(text="Отметить сдачу")
        ],
    ],
    resize_keyboard=True
)

subject = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Записаться"),
        ],
        [
            KeyboardButton(text="Посмотреть очередь"),
            KeyboardButton(text="Посмотреть очередь с док-вами"),
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)