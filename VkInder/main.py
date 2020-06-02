from VkInder.vkUser.vk_api_userclass import User
from VkInder.vkUser.check_settings import *
from pprint import pprint
from pymongo import MongoClient
import pandas as pd
import json







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
    top10_json = json.dumps(top10, ensure_ascii=False).encode("utf8")
    write_in_database(top10_collection, top10)
    
    pprint(json.loads(top10_json))
    with open('top3.json', 'w', encoding='utf8') as file:
        data = json.loads(top10_json)
        json.dump(data, file, ensure_ascii=False, indent=4)
        print('файл top3.json создан успешно')   



if __name__ == "__main__":
    fields = 'id, about, activities, books, city, common_count, country,\
              first_name, games, bdate, home_town, interests,\
              last_name, movies, music, tv'
    sex = sex_check()
    age_from = age_from_foo()
    age_to = age_to_foo()
    user = check_user_name()
    if user != 'Invalid user id':
        raw_users_list = user.search_users(fields, sex, age_from, age_to)['response']['items']
        client = MongoClient()
        users_DB = client['VK_Inder']
        users_DB.top10.drop()
        top10_collection = users_DB['top10']
        if sex == 1:
            users_collection_woman = users_DB['users_woman']
            main(users_collection_woman)
        elif sex == 2:
            users_collection_man = users_DB['users_man']
            main(users_collection_man)
        else:
            print('Не верно указан пол. Должно быть 1 или 2')
    else:
        print('Нет пользователя с указанныс id')
    
    