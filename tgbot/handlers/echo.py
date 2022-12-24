from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.keyboards.reply import menu, subject


async def bot_echo(message: types.Message):
    if (message.text in ["Си", "Тисд", "Птп"]):
        await message.answer(f"Вы выбрали предмет: {message.text}", reply_markup=subject)
    elif (message.text == "Назад"):
        await message.answer("Возвращаемся в меню", reply_markup=menu)
    elif (message.text == "Посмотреть свои позиции"):
        await message.answer("Вы не состоите в очередях")
    elif (message.text == "Отметить сдачу"):
        await message.answer("Вы не состоите в очередях")
    elif (message.text == "Посмотреть очередь" or message.text == "Посмотреть очередь с док-вами"):
        await message.answer("Очередь пуста")
    elif (message.text == "Записаться"):
        await message.answer("Временно нельзя :(")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo, )
