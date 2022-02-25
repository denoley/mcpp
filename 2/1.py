# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.+
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

from bs4 import BeautifulSoup
import requests
import json
import time
from pprint import pprint
import pandas as pd

base_url = 'https://hh.ru/vacancy/'
vacancy_ids = [52916604 + i * 10 for i in range(0, 10)]
result = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

for i in vacancy_ids:
    response = requests.get(f'{base_url}{i}', headers=headers)
    if response.ok:
        vacancy = {}
        content = response.content.decode(encoding=response.encoding)
        dom = BeautifulSoup(content, 'html.parser')

        s = dom.find('script', {'type': 'application/ld+json'})

        j = json.loads(s.text)

        vacancy['title'] = j['title']
        if 'baseSalary' in j:
            if 'value' in j['baseSalary']:
                vacancy['salary_from'] = j.get('baseSalary').get('value').get('minValue')
                vacancy['salary_to'] = j.get('baseSalary').get('value').get('maxValue')
            vacancy['currency'] = j.get('baseSalary').get('currency')
        vacancy['organization'] = j['hiringOrganization']['name']
        vacancy['url'] = f'{base_url}{i}'

        result.append(vacancy)

with open('hh.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)

df = pd.DataFrame(result)
print(df)
