# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

def insert_to_mdb(vac_lst):
    client = MongoClient('localhost', 27017)
    db = client['vacancy']
    vacancy = db.vacancy

    for i in vac_lst:
        if not  vacancy.find_one({'id': i['id']}):
            vacancy.insert_one(i)
            print(i['title'],'добавлена в БД')

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
        vacancy['id'] = i

        result.append(vacancy)


# Заполнили список вакансий

# with open('hh.json', 'w') as f:
#     json.dump(result, f, ensure_ascii=False)

df = pd.DataFrame(result)
print(df)

insert_to_mdb(result)