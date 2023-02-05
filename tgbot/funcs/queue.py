# Очередь представлена в queue_data.pkl.
# Содержит массив - [[айди, предмет, описание заявки, время записи], ...].
# Айди - int, Предмет - str, Описание - str, Время - float
#
# Информация о пользователях содержится в users_data.json.
# Содержит информацию об айди, фамилии, имени и статусе пользователя (студент/что-то другое)
# Айди - str, Фамилия - str, Имя - str, Статус - str.
#
# Информация о предметах содержится в subjects_data.json
# Ключом является аббревиатура предмета, значением его расшифровка
# Ключ - str, Расшифровка - str
#
#
# Основные функции для работы - queue_add, queue_del, queue_make/queue_msg.
#
import time
import datetime
from tgbot.funcs.read_check import *


# Запись очереди в файл. Время генерируется автоматически.
# @param usr_id - ID человека
# @param subj - Имя предмета (пример - "OOP")
# @param name - Описание типа заявки (пример - "ЛР3")
# @return 1 в случае успеха, иначе ошибка
def queue_add(usr_id: int, subj: str, name: str):
    request = [usr_id, subj, name, time.time()]

    # Проверка на корректность элемента
    rc = queue_check([request])
    if rc != 1:
        return rc

    queue_req = queue_read()

    # Проверка на корректность очереди
    rc = queue_check(queue_req)
    if rc != 1 and queue_req is not None:
        return rc
    if queue_req is None:
        queue_req = []

    # Проверка на наличие такого же описания с предметом в очереди
    for req in queue_req:
        if req[0] == request[0] and req[1] == request[1] and req[2] == request[2]:
            return 20

    queue_req.append(request)

    with open("./users_data/queue_data.pkl", "wb") as file:
        pickle.dump(queue_req, file)

    return 1


# Удаление заявки пользователя из файла queue_data.pkl
# @param usr_id - ID человека
# @param subj - Имя предмета (пример - "OOP")
# @param name - Описание типа заявки (пример - "ЛР3")
# @return 1 в случае успеха, иначе ошибка
def queue_del(usr_id: int, subj: str, name: str):
    queue_req = queue_read()

    rc = queue_check(queue_req)
    if rc != 1:
        return rc

    # Поиск подходящего элемента очереди
    for ind, req in enumerate(queue_req):
        if req[0] == usr_id and req[1] == subj and req[2] == name:
            del queue_req[ind]
            break
    else:
        return 2

    with open("./users_data/queue_data.pkl", "wb") as file:
        pickle.dump(queue_req, file)

    return 1


# Составление очереди по айди и/или предмету. Если оба параметра None - возвращается вся очередь
# @param usr_id - Айди пользователя (пример - 2026922, None).
# @param subj - Имя предмета (пример - "OOP", None).
# @return Упорядоченный массив типа [Айди, предмет, описание, время записи] в случае успеха, код ошибки в противном случае
def queue_make(usr_id: int, subj: str):
    usr_flag, subj_flag = 0, 0

    if usr_id is not None:
        usr_flag = 1
        if str(usr_id) not in users_read().keys():
            return 32

    if subj is not None:
        subj_flag = 1
        if subj not in subjects_read().keys():
            return 33

    queue_req = queue_read()

    rc = queue_check(queue_req)
    if rc != 1:
        return rc

    arr_req = []

    for req in queue_req:
        if usr_flag and req[0] == usr_id and subj_flag and req[1] == subj:
            arr_req.append(req)
        elif not subj_flag and usr_flag and req[0] == usr_id:
            arr_req.append(req)
        elif not usr_flag and subj_flag and req[1] == subj:
            arr_req.append(req)
        elif not usr_flag and not subj_flag:
            arr_req.append(req)
    # print(arr_req)

    arr_req.sort(key=lambda x: x[3])

    return arr_req


# Оформление очереди в виде сообщения. Возвращает форматированную строку. Если оба параметра None - возвращается вся очередь
# @param usr_id - Айди пользователя (пример - 2026922, None).
# @param subj - Ключ предмета (пример - "OOP", None).
# @return Форматированная строка в случае успеха, код ошибки в противном случае
def queue_msg(usr_id: int, subj: str):
    msg = ""
    users = users_read()

    rc = users_check(users)
    if rc != 1:
        return 1

    queue_req = queue_make(usr_id, subj)

    if type(queue_req) != list:
        return 2

    ind = 1
    subjects = subjects_read()

    for req in queue_req:
        # usr_info - информация о пользователе в users_data
        usr_info = users[str(req[0])]
        timestamp = datetime.datetime.fromtimestamp(req[3])
        usr_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        user_str = "{}. {:8} {}.  {:5} {:5}\n{}\t\n".format(ind, usr_info["f_name"], usr_info["l_name"]
                                                              [0], subjects[req[1]], req[2], usr_time)
        msg += user_str
        ind += 1

    return msg


# users_info = users_read()
