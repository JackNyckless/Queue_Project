from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import menu


async def admin_start(message: Message):
    await message.reply("Привет, студент-админ!", reply_markup=menu)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
