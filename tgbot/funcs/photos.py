# Функции для работы с фотографиями (доказательствами)
#
# Основные функции для работы - photo_name.
#

# Получение имени фотографии по входным данным
# @param usr_id - ID человека
# @param subj - Имя предмета (пример - "OOP")
# @param time_req - время подачи заявки в очередь
# @return название фотографии
def photo_name(usr_id: int, subj: str, time_req: float):
    return './users_data/photos/{}_{}_{}.png'.format(subj, usr_id, int(time_req))

# print(photo_name(121, 'Ilya', 117.118))