from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.reply import main_menu
from tgbot.funcs.queue import *
from tgbot.funcs.photos import *
import logging
import os

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
    await message.answer("Список команд:\n\n" +
        "/users (список студентов)\n" +\
        "/users_add (добавление пользователя, 4 параметра:\n\
            \t1. ID в Телеграме\n\
            \t2. Фамилия\n\
            \t3. Имя\n\
            \t4. Статус (например, student))\n" +\
        "/users_del (удаление пользователя, 1 параметр:\n\
            \t-> Номер позиции в списке пользователей)\n" +\
        "/subjects (список предметов)\n" +\
        "/queue (проверить очередь)\n" +\
        "/queue_del (удаление позиции из очереди, 1 параметр:\n\
            \t-> Номер позиции в полной очереди)\n" +\
        "/queue_watch (просмотр позиции с доказательством, 1 параметр:\n\
            \t-> Номер позиции в полной очереди)")


async def admin_cmds(message: Message):
    words = list(map(str, message.text.split()))
    cmd = words[0].replace("/", "")

    if cmd == "users":
        users = users_read()
        msg = "Список пользователей:\n"

        for ind, user in enumerate(users):
            msg += "{}. {} {}: \n{}({})\n".format(ind + 1, users[user]['l_name'],\
                users[user]['f_name'], user,users[user]['status'])

        await message.answer(msg)
    elif cmd == "users_add":
        msg = ""
        users = users_read()

        if len(words) > 1 and words[1] in users:
            msg = "Пользователь с данным ID уже есть в базе данных."

        if not msg and len(words) == 5 and words[1].isdigit() and int(words[1]) != 0:
            user = {"l_name": words[2], \
                "f_name": words[3], \
                "status": words[4]}
            users[words[1]] = user

            with open("./users_data/users_data.json", "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4, ensure_ascii=False)

            msg = "Пользователь успешно добавлен"
        elif not msg:
            msg = "Вы ввели некорректные данные."

        await message.answer(msg)
    elif cmd == "users_del":
        msg = "Вы ввели некорректные данные"

        if len(words) == 2 and words[1].isdigit() and int(words[1]) != 0:
            index_del = int(words[1]) - 1
            users = users_read()

            if (index_del >= len(users)):
                msg = "Пользователя с таким номером не существует."
            else:
                users.pop(list(users)[index_del])

                with open("./users_data/users_data.json", "w", encoding="utf-8") as file:
                    json.dump(users, file, indent=4, ensure_ascii=False)

                msg = "Удаление успешно завершено."

        await message.answer(msg)
    elif cmd == "subjects":
        subjects = subjects_read()
        msg = "Список предметов:\n"

        for ind, subject in enumerate(subjects):
            msg += "{}. {}: {}\n".format(ind + 1, subject, subjects[subject])

        await message.answer(msg)
    elif cmd == "queue":
        msg = "Полная очередь:\n"
        full_queue = queue_msg(None, None)

        if not full_queue:
            full_queue = "Очередь пуста."

        msg += full_queue

        await message.answer(msg)
    elif cmd == "queue_del":
        msg = "Вы ввели некорректные данные"

        if len(words) == 2 and words[1].isdigit() and int(words[1]) != 0:
            index_del = int(words[1]) - 1
            queue_req = queue_read()

            if (index_del >= len(queue_req)):
                msg = "Позиции с таким номером не существует."
            else:
                queue_del(queue_req[index_del][0], queue_req[index_del][1], queue_req[index_del][2])
                os.remove(photo_name(queue_req[index_del][0], queue_req[index_del][1], queue_req[index_del][3]))

                msg = "Удаление успешно завершено."

        await message.answer(msg)
    elif cmd == "queue_watch":
        msg = "Вы ввели некорректные данные"

        if len(words) == 2 and words[1].isdigit() and int(words[1]) != 0:
            index_del = int(words[1]) - 1
            queue_req = queue_read()

            if (index_del >= len(queue_req)):
                msg = "Позиции с таким номером не существует."
                await message.answer(msg)
            else:
                name = photo_name(queue_req[index_del][0], queue_req[index_del][1], queue_req[index_del][3])
                msg = list(map(str, queue_msg(None, None).split("\n")))[index_del]

                await message.answer_photo(open(name, 'rb'), caption=msg)
        else:
            await message.answer(msg)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=[
                                "start"], state="*", is_admin=True)
    dp.register_message_handler(admin_help, commands=[
                                "help"], state="*", is_admin=True)
    dp.register_message_handler(admin_cmds, commands=[
                                "users", "users_add", "users_del", "subjects", "queue",
                                "queue_del", "queue_watch"], state="*", is_admin=True)
