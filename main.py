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
user_name = input('Введите имя пользователя: ')
user = User(user_name)
user_groups_list = user.get_groups_ids()
#дикт с данными о пользователе
user_info = user.get_info_about_me(fields)['response'][0]
#сырой список кандидатов
raw_users_list = user.search_users(fields, sex, age_from, age_to)['response']['items']



#функция получения id пользователей из БД
def check_user_id(db):
    '''
    получаем данные из коллекции, если коллекция не пустая - создаем список id
    пользователей которые есть в коллекции и возвращаем список id.
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
def panda_analis(single_user_db, many_users_db):
    user_df = pd.DataFrame(list(single_user_db.find())).set_index('id')
    users_df = pd.DataFrame(list(many_users_db.find())).set_index('id')

    #получаем год рождения основного пользователя
    for i in user_df['bdate']:
        user_bdate = i.split('.')[2]
    
    users_df['points'] = 0
    
    #делаем ссылку на профиль каждого пользователя
    for i in users_df.index:
        users_df.loc[users_df.index == i, 'href'] = f'https://vk.com/id{i}'

    #создаем списки пользователя
    for i in user_df.T.iteritems():
        user_music_list = i[1][30].split(', ')
        user_films_list = i[1][32].split(', ')
        user_books_list = i[1][34].split(', ')
        user_games_list = i[1][29].split(', ')

    #проверяем год рождения
    for i in users_df.T.iteritems():
        if i[1][6].split('.')[2] == user_bdate:
            users_df.loc[users_df.index == i[0], 'points'] += 4

    #ищем общие группы
    for i in user_df.T.iteritems():
        users_id = i[0]
        users_groups = User(users_id).get_groups_ids()
        for group_id in user_groups_list:
            if group_id in users_groups:
                users_df.loc[users_df.index == i[0], 'points'] += 3
    
    # ищем общие книжки
    for book in user_books_list:
        book = book.lower()
        for i in users_df.T.iteritems():
            if book in str(i[1][32]).lower():
                users_df.loc[users_df.index == i[0], 'points'] += 1

    #ищем общих друзей
    for i in users_df.T.iteritems():
        if i[1][15] > 0:
            users_df.loc[users_df.index == i[0], 'points'] += 5
    
    #ищем общую музыку
    for music in user_music_list:
        music = music.lower()
        for i in users_df.T.iteritems():
            if music in str(i[1][28]).lower():
                users_df.loc[users_df.index == i[0], 'points'] += 2

    #ищем общие фильмы
    for film in user_films_list:
        film = film.lower()
        for i in users_df.T.iteritems():
            if film in str(i[1][30]).lower():
                users_df.loc[users_df.index == i[0], 'points'] += 2

    # #ищем общие игры
    for game in user_games_list:
        game = game.lower()
        for i in users_df.T.iteritems():
            if game in str(i[1][33]).lower():
                users_df.loc[users_df.index == i[0], 'points'] += 1
        
    top10 = users_df[users_df['points'] > 0].sort_values(['points'], ascending=False).head(10)
    return top10



def main():
    lst = filter_users(users_collection, raw_users_list)
    lst2 = filter_users(user_collection, [user_info])
    write_in_database(users_collection, lst)
    write_in_database(user_collection, lst2)

    filter = ['first_name', 'last_name', 'points', 'href']
    print(panda_analis(user_collection, users_collection)[filter])



if __name__ == "__main__":
    client = MongoClient()
    users_DB = client['VK_Inder']
    users_collection = users_DB['users']
    user_collection_name = input('Введите название коллекции: ')
    user_collection = users_DB[user_collection_name]
    main()