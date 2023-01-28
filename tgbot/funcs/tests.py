from queue import *
from read_check import *


# Восстановление очереди в файле
def queue_repair(queue_copy: list):
    with open("../queue_data.pkl", "wb") as file:
        pickle.dump(queue_copy, file)


# Тесты
def main_tests():
    users = list(map(int, users_read().keys()))
    subjects = list(subjects_read().keys())
    print("Users - ", users)
    print("Subjects - ", subjects)

    # print("Before - ", queue_read())
    print("\n")

    # Добавление обычной заявки пользователя
    msg = "Added usual request"
    if queue_add(users[0], subjects[0], "LR10") != 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Удаление обычной заявки пользователя
        msg = "Delete usual request"
        if queue_del(users[0], subjects[0], "LR10") != 1:
            print("ERROR: " + msg)
        else:
            print("SUCCESS: " + msg)

    # Добавление в очередь несуществующего пользователя
    msg = "Added unknown user to queue"
    if queue_add(-1, subjects[0], "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Добавление в очередь несуществующего предмета
    msg = "Added unknown subject to queue"
    if queue_add(users[0], "weqrkmfwockemfro", "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Добавление в очередь несуществующего пользователя и предмета
    msg = "Added unknown user and subject to queue"
    if queue_add(-1, "qowkepdeqmf", "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Добавление в очередь уже существующую заявку по предмету о описанию
    msg = "Added two equal request to queue"
    if queue_add(users[0], subjects[1], "LR1") == 1 and queue_add(users[0], subjects[1], "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    queue_del(users[0], subjects[1], "LR1")

    # Удаление заявки у несуществующего пользователя
    msg = "Delete request from unknown user"
    if queue_del(-1, subjects[0], "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Удаление заявки с несуществующим предметом
    msg = "Delete request with unknown subject"
    if queue_del(users[0], "QWKMDSDKWQMD", "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Удаление заявки у несуществующего пользователя с несуществующим предметом
    msg = "Delete request from unknown user with unknown subject"
    if queue_del(-1, "QWKMDSDKWQMD", "LR1") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    # Удаление заявки у пользователя с предметом, но отличающимся описанием
    msg = "Delete request from user, but another description"
    queue_add(users[0], subjects[1], "LR13")
    if queue_del(users[0], subjects[1], "LR15") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)
    queue_del(users[0], subjects[1], "LR13")
    # Удаление заявки дважды
    msg = "Delete request twice"
    queue_add(users[0], subjects[1], "LR5")
    if queue_del(users[0], subjects[1], "LR5") == 1 and queue_del(users[0], subjects[1], "LR5") == 1:
        print("ERROR: " + msg)
    else:
        print("SUCCESS: " + msg)

    # print("\n")
    # print("After -  ", queue_read())


# Тестирование
queue_copy = queue_read()
try:
    main_tests()
except Exception:
    pass
queue_repair(queue_copy)
