from vk_api_userclass import User
from pprint import pprint
from datetime import datetime, date
import time



tihon = User('tihon333')
den = User('vindevi')
friends_ids_list = tihon.get_friends()
bd_friends_names_and_age = []

fields = 'sex, bdate, city, country, home_town, contacts, education,' \ 
         'career, military, universities, schools, status, is_friend' \
         ',common_count, relatives, relation, personal, connections,' \ 
         'wall_comments, activities, interests, music, movies, tv,' \
         'books, games, about, quotes'

# for group_name in tihon.get_groups()['response']['items']:
#     print(group_name['name'])

user_bd = datetime.strptime('11.12.1985', '%d.%m.%Y').date()


#функция поиска подходящих по возрасту друзей
def check_age_limit(current_user):
    curent_age =  datetime.strptime(current_user['response'][0]['bdate'], '%d.%m.%Y').date()
    difference = str(user_bd - curent_age).split()[0]
    print(difference)
    if (int(difference) / 365) > 3:
        print(f'старше больше чем на три года\nдата: {current_user["response"][0]["bdate"]}')
        return False
    elif (int(difference) / 365) < -3:
        print(f'младше больше чем на три года\nдата: {current_user["response"][0]["bdate"]}')
        return False
    else:
        print(f'подходит: {current_user["response"][0]["bdate"]}')
        return True



for f_id in friends_ids_list:
    current_user_info = User(f_id).get_user_info()
    # print('.', end='')
    if current_user_info and len(current_user_info['response'][0]['bdate'].split('.')) == 3 and check_age_limit(current_user_info):
        bd_friends_names_and_age.append(current_user_info['response'][0])
        print(f'подходящих друзей => {len(bd_friends_names_and_age)}')
        



pprint(bd_friends_names_and_age)