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
from read_check import *


# Запись очереди в файл. Время генерируется автоматически.
# @param usr_id - ID человека
# @param subj - Имя предмета (пример - "OOP")
# @param name - Описание типа заявки (пример - "ЛР3")
# @return 1 в случае успеха, иначе ошибка
def queue_add(usr_id: int, subj: str, name: str):
    array = [usr_id, subj, name, time.time()]
    # Проверка на корректность элемента
    res = queue_check([array])
    if res != 1:
        return res

    qe = queue_read()
    # Проверка на корректность очереди
    res = queue_check(qe)
    if res != 1 and qe is not None:
        return res
    if qe is None:
        qe = []

    # Проверка на наличие такого же описания с предметом в очереди
    for re in qe:
        if re[0] == array[0] and re[1] == array[1] and re[2] == array[2]:
            return 20

    qe.append(array)
    with open("./users_data/queue_data.pkl", "wb") as file:
        pickle.dump(qe, file)
    return 1


# Удаление заявки пользователя из файла queue_data.pkl
# @param usr_id - ID человека
# @param subj - Имя предмета (пример - "OOP")
# @param name - Описание типа заявки (пример - "ЛР3")
# @return 1 в случае успеха, иначе ошибка
def queue_del(usr_id: int, subj: str, name: str):
    qe = queue_read()
    res = queue_check(qe)
    if res != 1:
        return res

    # Поиск подходящего элемента очереди
    ind_file = -1
    for i in range(len(qe)):
        if qe[i][0] == usr_id and qe[i][1] == subj and qe[i][2] == name:
            ind_file = i
            break
    if ind_file == -1:
        return 2

    del qe[ind_file]
    with open("./users_data/queue_data.pkl", "wb") as file:
        pickle.dump(qe, file)

    return 1


# Составление очереди по айди и/или предмету. Если оба параметра None - возвращается вся очередь
# @param usr_id - Айди пользователя (пример - 2026922, None).
# @param subj - Имя предмета (пример - "OOP", None).
# @return Упорядоченный массив типа [Айди, предмет, описание, время записи] в случае успеха, код ошибки в противном случае
def queue_make(usr_id: int, subj: str):
    if usr_id is not None:
        u_flag = 1
        if str(usr_id) not in users_read().keys():
            return 32
    else:
        u_flag = 0
    if subj is not None:
        s_flag = 1
        if subj not in subjects_read().keys():
            return 33
    else:
        s_flag = 0

    qe = queue_read()
    res = queue_check(qe)
    if res != 1:
        return res
    arr_qe = []

    for re in qe:
        if u_flag and re[0] == usr_id and s_flag and re[1] == subj:
            arr_qe.append(re)
        elif not s_flag and u_flag and re[0] == usr_id:
            arr_qe.append(re)
        elif not u_flag and s_flag and re[1] == subj:
            arr_qe.append(re)
        elif not u_flag and not s_flag:
            arr_qe.append(re)
    # print(arr_qe)
    arr_qe.sort(key=lambda x: x[3])

    return arr_qe


# Оформление очереди в виде сообщения. Возвращает форматированную строку. Если оба параметра None - возвращается вся очередь
# @param usr_id - Айди пользователя (пример - 2026922, None).
# @param subj - Ключ предмета (пример - "OOP", None).
# @return Форматированная строка в случае успеха, код ошибки в противном случае
def queue_msg(usr_id: int, subj: str):
    msg = ""
    users = users_read()
    res = users_check(users)
    if res != 1:
        return 1

    qe = queue_make(usr_id, subj)
    if type(qe) != list:
        return 2

    ind = 1
    subjects = subjects_read()
    for i in qe:
        # u_info - информация о пользователе в users_data
        u_info = users[str(i[0])]
        timestamp = datetime.datetime.fromtimestamp(i[3])
        u_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        user_str = "{}. {:8} {}. - {:5} - {:5} - {}\n".format(ind, u_info["f_name"], u_info["l_name"][0], subjects[i[1]], i[2], u_time)
        msg += user_str
        ind += 1

    return msg


# users_info = users_read()
