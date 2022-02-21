'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
'''
import requests

url = 'https://api.github.com/users/postgres/repos'

response = requests.get(url)

if response.ok:
    with open('postgres.json', 'w') as f:
        f.writelines(response.content.decode(encoding=response.encoding))
