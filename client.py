import requests

# response = requests.post(
#     'http://127.0.0.1:5000/adv',
#     json={'heading': 'Продам Мерседес', 'description': 'Продам автомобиль Мерседес A600, черный', 'creator': '2'},
#
# )
# print(response.status_code)
# print(response.json())
#
# response = requests.patch(
#     'http://127.0.0.1:5000/adv/7',
#     json={'description': 'Продам автомобиль Мерседес S600', 'creator': '14'},
#
# )
#
# response = requests.get(
#     'http://127.0.0.1:5000/adv/2',
#
# )



response = requests.delete(
    'http://127.0.0.1:5000/adv/1',
    json={'creator': '1'},

)


# response = requests.get(
#     'http://127.0.0.1:5000/user/14',
#
# )

# response = requests.post(
#     'http://127.0.0.1:5000/user',
#     json={'name': 'user_1', 'password': 'qwerty123', 'email': 'user@gmail.ru'},
#
# )
# print(response.status_code)
# print(response.json())

# response = requests.patch(
#     'http://127.0.0.1:5000/user/18',
#     json={'name': 'new_user', 'password': '123456789'},
#
# )
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     'http://127.0.0.1:5000/user/13',
#
# )
# print(response.status_code)
# print(response.json())
#
# response = requests.get(
#     'http://127.0.0.1:5000/adv/1',
#
# )

print(response.status_code)
print(response.json())