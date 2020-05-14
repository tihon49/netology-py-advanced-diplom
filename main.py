from vk_api_userclass import User
from pprint import pprint
from datetime import datetime, date
import time



fields = 'sex, bdate, city, country, home_town, contacts, education,'\
         'career, military, universities, schools, status, is_friend,'\
         'common_count, relatives, relation, personal, connections,'\
         'wall_comments, activities, interests, music, movies, tv,'\
         'books, games, about, quotes'
sex = 1
age_from = 25
age_to = 35

tihon = User('tihon333')
tihon_info = tihon.get_info_about_me(fields)['response'][0] #дикт с данными о пользователе

raw_users_list = tihon.search_users(fields, sex, age_from, age_to)
raw_users_list = raw_users_list['response']['items'] #сырой список кандидатов



#функция отбора кандидатов
def filter_users(users_list):
    pass
