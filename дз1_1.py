import requests
import json
from pprint import pprint

url = 'https://api.github.com/users/'
user_name = input("Введитие Имя Пользователя: ")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
          "Accept": "application/json"}

responce = requests.get(url + user_name + "/repos", headers=headers)

if responce.status_code < 399:
    j_repos = responce.json()
    print(f'У Пользователя {user_name} на  GitHub имеется {len(j_repos)} репозитория')
    print('Список всех репозиториев:')
    for i in j_repos:
        pprint(i.get("name"))
else:
    print(responce.status_code)

with open('data.txt', 'w') as outfile:
    json.dump(j_repos, outfile)