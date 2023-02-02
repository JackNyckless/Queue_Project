from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import menu
from tgbot.funcs.queue import *


async def admin_start(message: Message):
    users = dict(users_read())
    if users.get(str(message.from_user.id)):
        name = users.get(str(message.from_user.id))["f_name"]
    else:
        name = "неизвестный админ"
    await message.reply(f"Привет, {name}! 😎\n\nТебе доступны все возможности обычного студента 🧑‍🎓 и секретные админ-команды для работы с ботом 🤖\n\nКоманды: /help", reply_markup=menu)


async def admin_help(message: Message):
    await message.answer("Список команд:\n\n/users (список студентов)\n/admins (список админов)\n/subjects (список предметов)\n/queue (проверить очередь)")


async def admin_users(message: Message):
    await message.answer(str(users_read()))


async def admin_subjects(message: Message):
    await message.answer(str(subjects_read()))


async def admin_queue(message: Message):
    await message.answer(str(queue_read()))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=[
                                "start"], state="*", is_admin=True)
    dp.register_message_handler(admin_help, commands=[
                                "help"], state="*", is_admin=True)
    dp.register_message_handler(admin_users, commands=[
                                "users"], state="*", is_admin=True)
    dp.register_message_handler(admin_subjects, commands=[
                                "subjects"], state="*", is_admin=True)
    dp.register_message_handler(admin_queue, commands=[
                                "queue"], state="*", is_admin=True)
