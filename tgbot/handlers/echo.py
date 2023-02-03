from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.keyboards.reply import main_menu, subject_menu, cancel_menu, confirm_menu
from tgbot.funcs.photos import *
from tgbot.funcs.queue import *
from tgbot.config import load_config
from tgbot.misc.states import Actions
import logging
import os

admins = load_config(".env.dist").tg_bot.admin_ids
logger = logging.getLogger(__name__)


# Бан использования для сторонних людей
async def user_access(message: types.Message, state: FSMContext):
    users = list(map(int, users_read().keys()))
    if message.from_user.id not in users and message.from_user.id not in admins:
        return
    await bot_echo(message, state=state)


# Основные кнопки бота
async def bot_echo(message: types.Message, state: FSMContext):
    subjects = subjects_read()
    subject = (await state.get_data()).get("subject")
    from_id = message.from_user.id
    msg = "Непонятное сообщение. Выберите пункт в меню."
    if subject:
        current_menu = subject_menu
    else:
        current_menu = main_menu

    if message.text in list(subjects.values()) and subject == None:
        await state.update_data(subject=list(subjects.keys())[list(
            subjects.values()).index(message.text)])
        msg = f"Вы выбрали предмет: {message.text}"
        current_menu = subject_menu
    elif message.text == "Назад" and subject != None:
        await state.update_data(subject=None)
        msg = "Возвращаемся в меню"
        current_menu = main_menu
    elif message.text == "Посмотреть свои позиции" and subject == None:
        msg = queue_msg(from_id, None)
        if not msg:
            msg = "Вы не состоите ни в одной очереди"
    elif message.text == "Отметить сдачу" and subject == None:
        if queue_make(from_id, None):
            msg = f"Вот список ваших сдач:\n\n{queue_msg(from_id, None)}\nНапишите номер работы, которую вы уже сдали 🔢"
            await Actions.REMOVE.set()
            current_menu = cancel_menu
        else:
            current_menu = main_menu
            msg = "Вы не состоите ни в одной очереди"
    elif message.text == "Посмотреть очередь" and subject != None:
        msg = queue_msg(None, subject)
        if not msg:
            msg = "Очередь пустая"
    elif message.text == "Посмотреть очередь с док-вами" and subject != None:
        msg = queue_msg(None, subject)
        if not msg:
            msg = "Очередь пустая"
        else:
            msg_split = msg.split("\n")
            works = queue_make(None, subject)
            for i, work in enumerate(works):
                name = photo_name(work[0], subject, work[3])
                await message.answer_photo(open(name, 'rb'), caption=msg_split[i])
            msg = None
    elif message.text == "Записаться" and subject != None:
        await Actions.ADD.set()
        msg = "Введите название работы (лабораторная/домашняя и номер) и прикрепите к сообщению фото-доказательство"
        current_menu = cancel_menu

    if msg:
        await message.answer(msg, reply_markup=current_menu)
    else:
        msg = "Вывел очередь с док-вами"
    if msg == queue_msg(None, subject):
        msg = "Вывел очередь без док-в"
    if queue_msg(from_id, None) in msg:
        msg = "Вывел ваши позиции"
    logger.info(f"New message from ID{from_id}: {message.text}")
    logger.info(f"Bot answer to ID{from_id}: {msg}")


async def bot_add_echo(message: types.Message, state: FSMContext):
    from_id = message.from_user.id
    current_menu = cancel_menu
    subject = (await state.get_data()).get("subject")
    msg = "Вы не выбрали предмет"

    if message.text and message.text != "Отмена":
        msg = "Вы не прислали фото-доказательство"
    elif not message.text and not message.caption:
        msg = "Вы не приписали к фото название работы"
    else:
        if message.text == "Отмена":
            msg = "Вы отменили запись в очередь ❌"
        elif subject:
            queue_add(from_id, subject, message.caption)
            name = photo_name(from_id, subject, queue_make(
                from_id, subject)[-1][3])
            await message.photo[-1].download(destination_file=name)
            msg = "Вы успешно записались ✅"
        current_menu = main_menu
        await state.finish()
    await message.answer(msg, reply_markup=current_menu)
    logger.info(f"New add request from ID{from_id}")
    logger.info(f"Bot answer to ID{from_id}: {msg}")


async def bot_remove_echo(message: types.Message, state: FSMContext):
    from_id = message.from_user.id
    current_menu = main_menu
    msg = "Вы отменили сдачу работы ❌"

    if message.text != "Отмена":
        works = queue_make(from_id, None)
        msg = "Некорретный номер работы"
        try:
            num_work = int(message.text)
            if (num_work > 0 or num_work <= len(works)):
                msg = "Вы уверены? ⚠️"
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
    logger.info(f"New remove request from ID{from_id}")
    logger.info(f"Bot answer to ID{from_id}: {msg}")


async def bot_confirm_echo(message: types.Message, state: FSMContext):
    from_id = message.from_user.id
    msg = "Вы отменили сдачу работы ❌"

    if message.text == "Да":
        num_work = (await state.get_data()).get("work")
        works = queue_make(from_id, None)
        res = queue_del(from_id,
                        works[num_work][1], works[num_work][2])
        name = photo_name(from_id,
                          works[num_work][1], works[num_work][3])
        os.remove(name)
        msg = "Поздравляем со сдачей работы! 🥳"
    await message.answer(msg, reply_markup=main_menu)
    await state.finish()
    logger.info(f"New confirm request from ID{from_id}")
    logger.info(f"Bot answer to ID{from_id}: {msg}")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(user_access, state=None)
    dp.register_message_handler(
        bot_add_echo, state=Actions.ADD, content_types=["photo", "text"])
    dp.register_message_handler(bot_remove_echo, state=Actions.REMOVE)
    dp.register_message_handler(bot_confirm_echo, state=Actions.CONFIRM)
