from vk_api_userclass import User
from pprint import pprint
import time



tihon = User('tihon333')
den = User('vindevi')
friends_ids_list = tihon.get_friends()
bd_friends_names_and_age = []

# for group_name in tihon.get_groups()['response']['items']:
#     print(group_name['name'])



for f_id in friends_ids_list:
    current_user_info = User(f_id).get_user_info()
    print('.', end='')
    if current_user_info and len(current_user_info['response'][0]['bdate'].split('.')) == 3:
        bd_friends_names_and_age.append(current_user_info['response'][0])
        print('+')



pprint(bd_friends_names_and_age)