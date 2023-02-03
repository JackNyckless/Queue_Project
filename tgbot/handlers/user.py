from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import main_menu
from tgbot.funcs.read_check import users_read
import logging

logger = logging.getLogger(__name__)


async def user_start(message: Message):
    from_id = message.from_user.id

    users = dict(users_read())
    if users.get(str(from_id)):
        name = users.get(str(from_id))["f_name"]
        await message.reply(f"Привет, {name}! 🎓\n\nТы есть в списке студентов, а значит можешь пользоваться ботом 🤖\n\n[ Используй меню снизу ]", reply_markup=main_menu)
        logger.info(f"New user ID{from_id} start - student")
    else:
        await message.reply("Привет, незнакомец! 👤\n\nТебя нет в базе студентов этого бота. Обратись, пожалуйста, к администратору в своей группе 💬")
        logger.info(f"New user ID{from_id} start - stranger")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
