from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tgbot.funcs.read_check import subjects_read


def full_main_menu(menu):
    subjects = list(subjects_read().values())
    subjects_count = len(subjects)

    if subjects_count % 3 != 1:
        for subject in subjects:
            menu.insert(KeyboardButton(text=subject))
    elif subjects_count == 1:
        menu.add(KeyboardButton(text=subjects[0]))
    else:
        for i in range(subjects_count - 4):
            menu.insert(KeyboardButton(text=subjects[i]))
        for i in range(4, 0, -1):
            menu.add(KeyboardButton(text=subjects[subjects_count - i])) if i % 2 == 0 else menu.insert(
                KeyboardButton(text=subjects[subjects_count - i]))

    menu.add(KeyboardButton(text="Посмотреть свои позиции"))
    menu.add(KeyboardButton(text="Отметить сдачу"))


main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True
)

full_main_menu(main_menu)

subject_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Записаться"),
        ],
        [
            KeyboardButton(text="Посмотреть очередь"),
            KeyboardButton(text="Посмотреть очередь с док-вами")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)


cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)


confirm_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True
)
