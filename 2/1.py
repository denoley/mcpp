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
import pandas as pd

search_url = 'https://api.hh.ru/vacancies?text='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

search_str = input('Введите наименование вакансии:\n')
response = requests.get(f'{search_url}{search_str}', headers=headers)
content = response.content.decode(encoding=response.encoding)

vacancy_ids = []
j = json.loads(content)

for i in j['items']:
    vacancy_ids.append(int(i['id']))

base_url = 'https://hh.ru/vacancy/'

result = []


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

'''
Введите наименование вакансии:
oracle developer
                                         title  ...                             url
0           Разработчик PL/SQL Oracle (remote)  ...  https://hh.ru/vacancy/52920831
1                           Разработчик Oracle  ...  https://hh.ru/vacancy/52039996
2                         Senior ETL Developer  ...  https://hh.ru/vacancy/52513175
3                    Разработчик PL/SQL,Oracle  ...  https://hh.ru/vacancy/52896576
4                    Разработчик Oracle PL/SQL  ...  https://hh.ru/vacancy/53076520
5                    Developer PL / SQL Oracle  ...  https://hh.ru/vacancy/52855084
6                      Oracle Data Base Expert  ...  https://hh.ru/vacancy/52367344
7                      Oracle/PL/SQL Developer  ...  https://hh.ru/vacancy/52210014
8                           Разработчик Oracle  ...  https://hh.ru/vacancy/48840394
9           Middle Database Developer (Oracle)  ...  https://hh.ru/vacancy/52527606
10  Senior Java разработчик (Продукт Big Data)  ...  https://hh.ru/vacancy/52840097
11                Програміст -PL/SQL Developer  ...  https://hh.ru/vacancy/52959394
12         Старший/ Ведущий разработчик Oracle  ...  https://hh.ru/vacancy/50177480
13                       Разработчик Oracle BI  ...  https://hh.ru/vacancy/50746642
14                          Разработчик Oracle  ...  https://hh.ru/vacancy/53088913
15                SQL developer/Разработчик БД  ...  https://hh.ru/vacancy/50651330
16                          Программист Oracle  ...  https://hh.ru/vacancy/53087520
17                 Программист Oracle (PL/SQL)  ...  https://hh.ru/vacancy/52102888
18                          Разработчик Oracle  ...  https://hh.ru/vacancy/48840395
19                            Java разработчик  ...  https://hh.ru/vacancy/52474604

[20 rows x 6 columns]
'''