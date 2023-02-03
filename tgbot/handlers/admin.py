from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import main_menu
from tgbot.funcs.queue import *
import logging

logger = logging.getLogger(__name__)


async def admin_start(message: Message):
    from_id = message.from_user.id

    users = dict(users_read())
    if users.get(str(from_id)):
        name = users.get(str(from_id))["f_name"]
    else:
        name = "неизвестный админ"
    await message.reply(f"Привет, {name}! 😎\n\nТебе доступны все возможности обычного студента 🧑‍🎓 и секретные админ-команды для работы с ботом 🤖\n\nКоманды: /help", reply_markup=main_menu)
    logger.info(f"New user ID{from_id} start - admin")


async def admin_help(message: Message):
    await message.answer("Список команд:\n\n/users (список студентов)\n/subjects (список предметов)\n/queue (проверить очередь)")


async def admin_cmds(message: Message):
    cmd = message.text.replace("/", "")

    if cmd == "users":
        await message.answer(str(users_read()))
    elif cmd == "subjects":
        await message.answer(str(subjects_read()))
    elif cmd == "queue":
        await message.answer(str(queue_read()))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=[
                                "start"], state="*", is_admin=True)
    dp.register_message_handler(admin_help, commands=[
                                "help"], state="*", is_admin=True)
    dp.register_message_handler(admin_cmds, commands=[
                                "users", "subjects", "queue"], state="*", is_admin=True)
