from vk_api_userclass import User
from pprint import pprint
from datetime import datetime, date
from pymongo import MongoClient
import pandas as pd



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


#поиск совпадений и начисление баллов
def get_points(user, df):
    """
    принимает экземпляр класса пользователя для
    которого осуществляется поиск, и дата фрейм
    с пользователями для проверки.
    """

    user_info = user.get_user_info()
    user_info = check_users_params(user)
    user_groups = user.get_groups_ids()
    
    count = 0
    for u_id in df.id:
        if count == 10:
            break

        curent_user = df.loc[df.id == u_id] 

        #music
        for music in pd.DataFrame(curent_user)['music']:
            for m in music.split(', '):
                if m.lower() in [i.lower() for i in user_info['music'].split(', ')]:
                    df.loc[df.id == u_id, 'points'] += 2
                    print(f'id{u_id} +2 music', m)
                
        #movies
        for movies in pd.DataFrame(curent_user)['movies']:
            for m in movies.split(', '):
                if m.lower() in [i.lower() for i in user_info['movies'].split(', ')]:
                    df.loc[df.id == u_id, 'points'] += 1
                    print(f'id{u_id} +1 movies', m)

        #games
        for games in pd.DataFrame(curent_user)['games']:
            for g in games.split(', '):
                if g.lower() in [i.lower() for i in user_info['games'].split(', ')]:
                    df.loc[df.id == u_id, 'points'] += 1
                    print(f'id{u_id} +1 games', g)
        
        #books
        for books in pd.DataFrame(curent_user)['books']:
            for b in books.split(', '):
                if b.lower() in [i.lower() for i in user_info['books'].split(', ')]:
                    df.loc[df.id == u_id, 'points'] += 1
                    print(f'id{u_id} +1 books', b)
                    
        #tv
        for tv in pd.DataFrame(curent_user)['tv']:
            for t in tv.split(', '):
                if t.lower() in [i.lower() for i in user_info['tv'].split(', ')]:
                    df.loc[df.id == u_id, 'points'] += 1
                    print(f'id{u_id} +1 tv', t)
        
        #bdate
        for bd in pd.DataFrame(curent_user)['bdate']:
            if bd.split('.')[2] == user_info['bdate']:
                df.loc[df.id == u_id, 'points'] += 4
                print(f"id{u_id} +4 bdate", bd.split('.')[2])
                
        #groups
        try:
            curent_user_groups = User(u_id).get_groups_ids()
            for group in user_groups:
                if group in curent_user_groups:
                    df.loc[df.id == u_id, 'points'] += 3
                    print(f'id{u_id} +3 group', group)
        except:
            pass

        print('.')
        count += 1

    top10 = df[df['points'] > 0].sort_values(['points'], ascending=False).head(10)
    create_hrefs(top10)
    new_filter = ['first_name', 'last_name', 'points', 'href']
    top10 = top10[new_filter] 
    return top10.to_dict('records')



#проверка ключей пользователя для user_info
def check_users_params(user):
    user_info = user.get_user_info()
    must_have_keys = ['music', 'movies', 'tv', 'games', 'books']
    is_keys = []
    for i in user_info:
        is_keys.append(i)
        
    for i in must_have_keys:
        if i not in is_keys:
            enter_value = input(f'отсутствуют данные в поле {i}\nвведите данные через запятую (минимум одно): ')
            user_info[i] = enter_value
            
    return user_info  



#запись в базу данных
def write_in_database(db, lst):
    '''если список не пустой => записываем его в ДБ'''
    if lst:
        db.insert_many(lst)
        print('В БД внесены данные')
    else:
        print('Нет данных для записи в БД')



def create_hrefs(df):
    for i in df.id:
        df.loc[df.id == i, 'href'] = f'https://vk.com/id{i}'



def main(users_collection):
    lst = filter_users(users_collection, raw_users_list)
    write_in_database(users_collection, lst)
    df = pd.DataFrame(list(users_collection.find()))
    filter = ['id', 'about', 'activities', 'books', 'city', 'common_count', 'country',
              'first_name', 'games', 'bdate', 'home_town', 'interests', 
              'last_name', 'movies', 'music', 'tv']
    df = df[filter]
    df['points'] = 0
    df = df.fillna('')
   
    top10 = get_points(user, df)
    write_in_database(top10_collection, top10)
    # pprint(top10)



if __name__ == "__main__":
    fields = 'id, about, activities, books, city, common_count, country,\
              first_name, games, bdate, home_town, interests,\
              last_name, movies, music, tv'
    sex = int(input('Укажите пол для поиска\nженский = 1\nмужской = 2\n=> '))
    age_from = int(input('Укажите минимальный возраст для поиска: '))
    age_to = int(input('Укажите максимальный возраст для поиска: '))
    user_name = input('Введите id пользователя для которого ищем кандидатуру: ')
    user = User(user_name)
    raw_users_list = user.search_users(fields, sex, age_from, age_to)['response']['items']
    client = MongoClient()
    users_DB = client['VK_Inder']
    users_DB.top10.drop()
    top10_collection = users_DB['top10']
    if sex == 1:
        users_collection_wooman = users_DB['users_wooman']
        main(users_collection_wooman)
    elif sex == 2:
        users_collection_man = users_DB['users_man']
        main(users_collection_man)
    else:
        print('Не верно указан пол. Должно быть 1 или 2')
    
    