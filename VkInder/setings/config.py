APP_TOKEN  = '0230c98a3ff7854c47a13174438bb0aff9db9037955819942f42fd2d3bdef85f2e968affd342fa823b65a' # токен приложения
APP_ID     = 7329381 
expires_in = 0
my_user_id = 4305103


DOMAIN       = 'vindevi'
USER         = 148226630 # Ден
MY_USER_ID   = 4305103   # мой ID


Tihon    = MY_USER_ID
Sanya    = 10837418
IgorT    = 12033108
SlavaT   = 11307880
PopovS   = 11012020
VitalS   = 4431184
Fedosova = 35652619



METHOD       = 'users.getSubscriptions' # варианты запросов: 'friends.getOnline' / 'users.get' / 'friends.get'
                                        # пример:  url = f'https://api.vk.com/method/{METHOD}'

# import threading
# Отдельный поток - обёртка для последующих функций
# def thread(my_func):
#     def wrapper(*args, **kwargs):
#         my_thread = threading.Thread (target=my_func, args=args, kwargs=kwargs)
#         my_thread.start()

#     return wrapper





url_to_get_access_token = 'https://oauth.vk.com/authorize?client_id=7329381&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,offline,photos,audio,video,status,wall,docs,groups,notifications,stats&response_type=token&v=5.52'
