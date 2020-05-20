from config import *
import requests
from pprint import pprint
import time
import json

access_token = APP_TOKEN  # токен приложения
app_id = APP_ID  # id приложения
VERSION = 5.103


# Задача №1
class User:
    def __init__(self, u_id):
        self.id = u_id

        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': u_id,
                  'v': VERSION
                  }

        data = self.get_response(url, params)

        if data.get('response'):
            self.id = data['response'][0]['id']
        elif data.get('error'):
            self.id = data['error']['error_msg']

    # при вызове функции print(user) вывод ссылки на его профиль в VK
    def __str__(self):
        if self.id == 'Invalid user id':
            return f'указанный id не существует'
        else:
            return f'https://vk.com/id{self.id}'

    # битовое И (x & y)
    def __and__(self, user2):
        if self.get_friends() and user2.get_friends():
            user_1_friends = self.get_friends()
            user_2_friends = user2.get_friends()
            common_friends = []

            for friend in user_1_friends:
                if friend in user_2_friends:
                    common_friends.append(User(friend))

            if common_friends:
                return common_friends
            else:
                return 'у данных пользователей нет общих друзей'
        else:
            return 'не валидный id'

    # отправка request'a / получение response'а
    def get_response(self, url, params):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            return data

    #получение данных текущего экземпляра класса
    # def get_info_about_me(self, fields):
    #     url = 'https://api.vk.com/method/users.get'
    #     params = {'access_token': access_token,
    #               'user_ids': self.id,
    #               'fields': fields,
    #               'v': VERSION
    #               }
    #     data = self.get_response(url, params)
    #     if data['response']:
    #         return data['response'][0]
    #     else:
    #         return 'Пользователь не найден'

    #поиск пользователей по заданным параметрам
    def search_users(self, fields, sex, age_from, age_to):
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': access_token,
                  'q': '',
                  'count': 1000,
                  'fields': fields,
                  'city': 1,
                  'country': 1,
                  'sex': sex,
                  'status': 6,
                  'age_from': age_from,
                  'age_to': age_to,
                  'v': VERSION
                  }
        data = self.get_response(url, params)
        return data
        
    #получаем инфо о пользователе если указан возраст
    def get_user_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': access_token,
                  'user_ids': self.id,
                  'fields': 'bdate, sex, city, country, relation, relatives, connections,' \
                            'interests, music, movies, tv, books, games, about , is_friend, friend_status, career, military',
                  'v': VERSION
                  }
        data = self.get_response(url, params)
        if data.get('response') and data['response'][0].get('bdate'):
            data['response'][0]['bdate'] = data['response'][0]['bdate'].split('.')[2]
            return data['response'][0]
        else:
            bdata = input('укажите год рождения пользователя (4 цифры): ')
            data['response'][0]['bdate'] = bdata
            return data['response'][0]

    # получаем количество друзей из группы. type => int
    def get_group_contacts_count(self, g_id):
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {'access_token': access_token,
                  'group_id': g_id,
                  'filter': 'friends',
                  'v': VERSION
                  }

        data = self.get_response(url, params)

        if data.get('response'):
            return data['response']['count']

    # получаем список групп в ктороых состоит только данный пользователь
    def get_uniq_groups(self):
        if self.get_groups() != 'не валидный id':
            groups_list = self.get_groups()
            uniqal_groups = []
            print(f'всего групп найдено: {len(groups_list)}')

            for group in groups_list:
                print('.', end='')
                time.sleep(1)
                count_of_friends = self.get_group_contacts_count(group['id'])

                if count_of_friends == 0:
                    g_data = {'name': group['name'],
                              'gid': group['id'],
                              'members_count': group['members_count']
                              }
                    uniqal_groups.append(g_data)

            if len(uniqal_groups) == 0:
                print('Done')
                print('не состоит ни в одной "уникальной" группе')
            else:
                with open('groups.json', 'w', encoding='utf8') as f:
                    json.dump(uniqal_groups, f, ensure_ascii=False)

                print('Done')
                print(f'"уникальных" групп найдено: {len(uniqal_groups)}')
                print('В папке со скриптом появился файл "groups.json"\n'
                      'вкотором записаны уникальные группы пользователя.')
        else:
            print('не валидный id')

    # получаем список групп пользователя. type => list
    def get_groups(self):
        url = f'https://api.vk.com/method/groups.get'
        params = {'access_token': access_token,
                  'user_id': self.id,
                  'extended': 1,
                  'fields': 'members_count,counters,contacts,city,country',
                  'count': 1000,
                  'v': VERSION
                  }

        data = self.get_response(url, params)

        # if data.get('error'):
        #     print(f"возникла ошибка с кодом: {data['error']['error_code']}")
        #     return 'не валидный id'
        # else:
        #     groups = data['response']['items']
        #     return groups
        
        return data


    #id всех групп пользователя
    def get_groups_ids(self):
        url = f'https://api.vk.com/method/groups.get'
        params = {'access_token': access_token,
                  'user_id': self.id,
                  'extended': 1,
                  'fields': 'members_count,counters,contacts,city,country',
                  'count': 1000,
                  'v': VERSION
                  }

        data = self.get_response(url, params)

        return [g['id'] for g in data['response']['items']]


    # получаем список с друзьями. type => list
    def get_friends(self):
        url = f'https://api.vk.com/method/friends.get'
        params = {'access_token': access_token,
                  'v': VERSION,
                  'user_id': self.id,
                  'order': 'hints',
                  'fields': 'nickname,domain,city,photo_200_orig,online',
                  'name_case': 'nom'
                  }

        data = self.get_response(url, params)

        if data.get('response'):
            friends_id = [friend['id'] for friend in data['response']['items'] if friend.get('id')]

            return friends_id
        else:
            return False

    # получаем список друзей онлайн. type => dict
    def get_friends_online(self):
        url = 'https://api.vk.com/method/friends.getOnline'
        params = {
            'access_token': access_token,
            'v': VERSION,
            'user_id': self.id
        }

        data = self.get_response(url, params)

        if data.get('error'):
            return 'не валидный id'
        else:
            return data['response']

    # найти друга с которым больше всего общих друзей
    def get_most_of_common_friends(self):
        max_count_of_friends = 0
        max_friends_id = 0

        if not self.get_friends():
            print('не валидный id')
        else:
            print('просьба набраться терпения, '
                  'это может занять несколько минут.\n', end='')
            friends_list = self.get_friends()

            for friend in friends_list:
                print('.', end='')
                time.sleep(1)
                common_f_count = len(User(self.id) & User(friend))
                friend_id = User(friend).id

                if common_f_count > max_count_of_friends:
                    max_count_of_friends = common_f_count
                    max_friends_id = friend_id

            print(f'\nбольше всего общих друзей с пользователем: '
                  f'id{max_friends_id} - {max_count_of_friends}', end='')


if __name__ == '__main__':
    user = User(10837418)
    groups = user.get_groups_ids()
    pprint(groups)