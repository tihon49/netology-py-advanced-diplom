from vk_api_userclass import User
from pprint import pprint
from datetime import datetime, date
from pymongo import MongoClient
import pandas as pd



fields = 'sex, bdate, city, country, home_town, contacts, education,'\
         'career, military, universities, schools, status, is_friend,'\
         'common_count, relatives, relation, personal, connections,'\
         'wall_comments, activities, interests, music, movies, tv,'\
         'books, games, about, quotes, photo_max'
sex = 1
age_from = 25
age_to = 35

tihon = User('tihon333')
tihon_info = tihon.get_info_about_me(fields)['response'][0] #дикт с данными о пользователе

raw_users_list = tihon.search_users(fields, sex, age_from, age_to)
raw_users_list = raw_users_list['response']['items'] #сырой список кандидатов



#функция получения id пользователей из БД
def check_user_id(db):
    '''
    получаем данные из ДБ, если ДБ не пустая - создаем список id
    пользователей которые есть в БД и возвращаем список id.
    '''
    users = list(db.find())
    users_ids = []
    if len(users) != 0:
        for u in users:
            users_ids.append(u['id'])
    
    return users_ids



#функция отбора кандидатов
def filter_users(db, users_list):
    '''
    исключаем повторяющихся юзеров по id
    отсеиваем тех у кого ДР указан не полностью
    возвращем список уникальных пользователей
    '''
    lst_to_check = check_user_id(db)    #список уже имеющихся id в БД
    lst_to_return = []
    count = 0
    for user in users_list:
        if user['id'] not in lst_to_check:  #если такого id нет в БД => добавляем user'а
            try:
                if len(user.get('bdate').split('.')) == 3:  #отсеиваем тех у кого ДР указан не полностью, прим.: (21.06) и т.д.
                    lst_to_return.append(user)
                    count += 1
            except AttributeError:
                pass
        else:
            pass
    
    print(f'добавлено {count} новых пользователей')
    return lst_to_return




#запись в базу данных
def write_in_database(db, lst):
    '''если список не пустой => записываем его в ДБ'''
    if lst:
        db.insert_many(lst)



#анализ данных
def panda_analis(db):
    #создаем дата фрейм
    cols = ['id', 'first_name', 'last_name', 'bdate', 'city.title', 'photo_max', 'is_friend',
            'twitter', 'instagram', 'university', 'home_town', 'relation', 'personal.smoking',
            'personal.alcohol', 'personal.religion_id', 'interests', 'music', 'activities',
            'movies','tv','books','games','universities','schools','about','relatives','quotes']
    # df = pd.read_csv('vk_inder.csv', usecols=cols).set_index('id')
    # df = pd.DataFrame(list(db.find()))
    # print(df.city)
    



def main():
    check_user_id(users_collection)
    lst = filter_users(users_collection, raw_users_list)
    write_in_database(users_collection, lst)
    panda_analis(users_collection)



if __name__ == "__main__":
    client = MongoClient()
    users_DB = client['VK_Inder']
    users_collection = users_DB['users']
    main()