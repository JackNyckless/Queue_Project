from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import menu
from tgbot.funcs.read_check import users_read


async def user_start(message: Message):
    users = dict(users_read())
    if users.get(str(message.from_user.id)):
        name = users.get(str(message.from_user.id))["f_name"]
        await message.reply(f"Привет, {name}! 🎓\n\nТы есть в списке студентов, а значит можешь пользоваться ботом 🤖\n\n[ Используй меню снизу ]", reply_markup=menu)
    else:
        await message.reply("Привет, незнакомец! 👤\n\nТебя нет в базе студентов этого бота. Обратись, пожалуйста, к администратору в своей группе 💬")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
