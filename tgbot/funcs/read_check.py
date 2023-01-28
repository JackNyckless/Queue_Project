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
import json
import os
import pickle


# Чтение файла subjects_data
# @return Словарь
def subjects_read():
    with open("../subjects_data.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    return users


# Чтение файла users_data
# @return Словарь
def users_read():
    with open("../users_data.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    return users


# Чтение очереди из файла
# @return Прочитанный массив, в случае ошибки None
def queue_read():
    if not os.path.isfile("../queue_data.pkl"):
        return None
    if os.path.getsize("../queue_data.pkl") == 0:
        return None
    with open("../queue_data.pkl", "rb") as file:
        return pickle.load(file)


# Проверка очереди на корректность.
# @param array - Массив очереди типа [айди, предмет, время записи, описание записи]
# @return 1 в случае успеха. Другое число в случае ошибки
def queue_check(array: list):
    if array is None:
        return 100
    for req in array:
        if len(req) != 4:
            return 12
        if type(req[0]) != int or type(req[1]) != str or type(req[2]) != str or type(req[3]) != float:
            return 13
        users = users_read().keys()
        if str(req[0]) not in users:
            return 14
        subjs = subjects_read().keys()
        if str(req[1]) not in subjs:
            return 15
        if req[3] <= 0:
            return 16

    return 1


# Проверка пользователя на валидность данных
# @param users - Словарь пользователя
# @return 1 - данные корректны, иначе ошибка
def user_check(user: dict):
    if not user.get("f_name") or type(user["f_name"]) != str:
        return 3
    if not user.get("l_name") or type(user["l_name"]) != str:
        return 4
    if user.get("status") is None:
        return 5

    return 1


# Проверка пользователeй на валидность данных
# @param users - Словарь для редактирования
# @param usr_id - ID человека
# @return 1 - данные корректны, иначе ошибка
def users_check(users: dict):
    for user in users:
        if not users.get(user):
            return 10
        try:
            if int(user) <= 0:
                return 11
        except Exception:
            return 12
        res = user_check(users[user])
        if res != 1:
            return res

    return 1