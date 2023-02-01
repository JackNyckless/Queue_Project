from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.keyboards.reply import menu, subject_menu, cancel_menu, confirm_menu
from tgbot.funcs.photos import *
from tgbot.funcs.queue import *
from tgbot.config import load_config
from tgbot.misc.states import Actions
import logging
import os

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
        message.text = list(subjects.keys())[list(
            subjects.values()).index(message.text)]
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
    elif (message.text == "Посмотреть очередь"):
        subject = (await state.get_data()).get("subject")
        msg = queue_msg(None, subject)
        if not msg:
            msg = "Очередь пустая"
        await message.answer(msg)
    elif (message.text == "Посмотреть очередь с док-вами"):
        subject = (await state.get_data()).get("subject")
        msg = queue_msg(None, subject)
        if not msg:
            msg = "Очередь пустая"
            await message.answer(msg)
            return
        msg = msg.split("\n")
        works = queue_make(None, subject)
        for i, work in enumerate(works):
            name = photo_name(message.from_user.id, subject, work[3])
            await message.answer_photo(open(name, 'rb'), caption=msg[i])
    elif (message.text == "Записаться"):
        await Actions.ADD.set()
        await message.answer("Введите название работы (лабораторная/домашняя и номер) и прикрепите к сообщению фото-доказательство", reply_markup=cancel_menu)
    logger.info(f"New message from ID{message.from_user.id}: {message.text}")


async def bot_add_echo(message: types.Message, state: FSMContext):
    if (message.text and message.text != "Отмена"):
        msg = "Вы не прислали фото-доказательство"
        current_menu = cancel_menu
    elif (not message.text and not message.caption):
        msg = "Вы не приписали к фото название работы"
        current_menu = cancel_menu
    elif (message.text == "Отмена"):
        msg = "Вы отменили запись в очередь"
        current_menu = menu
        await state.finish()
    else:
        subject = (await state.get_data()).get("subject")
        current_menu = menu
        if subject == None:
            msg = "Вы не выбрали предмет"
        else:
            queue_add(message.from_user.id, subject, message.caption)
            name = photo_name(message.from_user.id, subject, queue_make(
                message.from_user.id, subject)[-1][3])
            await message.photo[-1].download(destination_file=name)
            msg = "Вы успешно записались"
        await state.finish()
    await message.answer(msg, reply_markup=current_menu)


async def bot_remove_echo(message: types.Message, state: FSMContext):
    msg = "Вы отменили сдачу работы"
    current_menu = menu
    if (message.text != "Отмена"):
        works = queue_make(message.from_user.id, None)
        msg = "Некорретный номер работы"
        try:
            num_work = int(message.text)
            if (num_work > 0 or num_work <= len(works)):
                msg = "Вы уверены?"
                current_menu = confirm_menu
                await Actions.CONFIRM.set()
                await state.update_data(work=num_work - 1)
            else:
                await state.finish()
        except:
            await state.finish()
    else:
        await state.finish()
    await message.answer(msg, reply_markup=current_menu)


async def bot_confirm_echo(message: types.Message, state: FSMContext):
    msg = "Вы отменили сдачу работы"
    if (message.text == "Да"):
        num_work = (await state.get_data()).get("work")
        works = queue_make(message.from_user.id, None)
        res = queue_del(message.from_user.id,
                        works[num_work][1], works[num_work][2])
        name = photo_name(message.from_user.id,
                          works[num_work][1], works[num_work][3])
        os.remove(name)
        msg = "Поздравляем со сдачей работы! 🥳"
    await message.answer(msg, reply_markup=menu)
    await state.finish()


def register_echo(dp: Dispatcher):
    dp.register_message_handler(user_access, state=None)
    dp.register_message_handler(
        bot_add_echo, state=Actions.ADD, content_types=["photo", "text"])
    dp.register_message_handler(bot_remove_echo, state=Actions.REMOVE)
    dp.register_message_handler(bot_confirm_echo, state=Actions.CONFIRM)
