from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.keyboards.reply import menu, subject_menu, cancel_menu
from tgbot.funcs.queue import *
from tgbot.config import load_config
from tgbot.misc.states import Actions
import logging

admins = load_config(".env.dist").tg_bot.admin_ids
logger = logging.getLogger(__name__)


async def user_access(message: types.Message, state: FSMContext):
    users = list(map(int, users_read().keys()))
    if message.from_user.id not in users and message.from_user.id not in admins:
        return
    await bot_echo(message, state=state)


async def bot_echo(message: types.Message, state: FSMContext):
    subjects = subjects_read()
    if (message.text in list(subjects.values())):
        await state.update_data(subject=list(subjects.keys())[list(
            subjects.values()).index(message.text)])
        await message.answer(f"Вы выбрали предмет: {message.text}", reply_markup=subject_menu)
    elif (message.text == "Назад"):
        await message.answer("Возвращаемся в меню", reply_markup=menu)
    elif (message.text == "Посмотреть свои позиции"):
        msg = queue_msg(message.from_user.id, None)
        if not msg:
            msg = "Вы не состоите ни в одной очереди"
        await message.answer(msg)
    elif (message.text == "Отметить сдачу"):
        msg = "Вы не состоите ни в одной очереди"
        if queue_make(message.from_user.id, None):
            msg = f"Вот список ваших сдач:\n\n{queue_msg(message.from_user.id, None)}\nНапишите номер работы, которую вы уже сдали 🔢"
            await Actions.REMOVE.set()
            current_menu = cancel_menu
        else:
            current_menu = menu
        await message.answer(msg, reply_markup=current_menu)
    elif (message.text == "Посмотреть очередь" or message.text == "Посмотреть очередь с док-вами"):
        msg = queue_msg(None, (await state.get_data()).get("subject"))
        if not msg:
            msg = "Очередь пустая"
        await message.answer(msg)
    elif (message.text == "Записаться"):
        await Actions.ADD.set()
        await message.answer("Введите название работы (лабораторная/домашняя и номер) и прикрепите к сообщению фото-доказательство", reply_markup=cancel_menu)
    logger.info(f"New message from ID{message.from_user.id}: {message.text}")


async def bot_add_echo(message: types.Message, state: FSMContext):
    msg = "Вы отменили запись в очередь"
    if (message.text != "Отмена"):
        subject = (await state.get_data()).get("subject")
        if subject == None:
            msg = "Вы не выбрали предмет"
        else:
            await message.photo[-1].download(destination_file='data/photos/test.jpg')
            queue_add(message.from_user.id, subject, message.text)
            msg = "Вы успешно записались"
    await message.answer(msg, reply_markup=menu)
    await state.finish()


async def bot_remove_echo(message: types.Message, state: FSMContext):
    msg = "Вы отменили сдачу работы"
    if (message.text != "Отмена"):
        works = queue_make(message.from_user.id, None)
        msg = "Некорретный номер работы"
        try:
            num_work = int(message.text)
            if (num_work > 0 or num_work <= len(works)):
                print(works)
                res = queue_del(message.from_user.id,
                                works[num_work-1][1], works[num_work-1][2])
                msg = "Поздравляем со сдачей работы! 🥳"
        except:
            None
    await message.answer(msg, reply_markup=menu)
    await state.finish()


def register_echo(dp: Dispatcher):
    dp.register_message_handler(user_access, state=None)
    dp.register_message_handler(
        bot_add_echo, state=Actions.ADD, content_types=['photo'])
    dp.register_message_handler(bot_remove_echo, state=Actions.REMOVE)
