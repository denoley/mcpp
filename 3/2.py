# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
# Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного
# (то есть цифра вводится одна, а запрос проверяет оба поля)

from pymongo import MongoClient

def find_by_salary(salary):
    client = MongoClient('localhost', 27017)
    db = client['vacancy']
    vacancy = db.vacancy

    for doc in vacancy.find({'$or': [{'salary_from': {'$gte': salary}}, {'salary_to': {'$gte': salary}}]},
                            {'organization': 1, 'title': 1, 'salary_from': 1, 'salary_to': 1, '_id': 0}):
        print(doc)


salary = int(input('Введите минимальную зарплату:\n'))
find_by_salary(salary)

'''
Введите минимальную зарплату:
100000
{'title': 'Разработчик DWH/OLAP', 'salary_from': 230000, 'salary_to': None, 'organization': 'NBCom Group'}
{'title': 'DWH Developer', 'salary_from': 150000, 'salary_to': None, 'organization': 'Dataduck'}
{'title': 'Senior DWH Developer / DWH Architect (TIP Team)', 'salary_from': 250000, 'salary_to': None, 'organization': 'Semrush'}
{'title': 'Разработчик хранилища данных (DWH), удаленная работа', 'salary_from': 230000, 'salary_to': None, 'organization': 'Фин тех проект федерального масштаба'}
{'title': 'Системный аналитик DWH (удаленно)', 'salary_from': 180000, 'salary_to': 300000, 'organization': 'РНД поинт'}
{'title': 'Разработчик DWH (MS SQL)', 'salary_from': 230000, 'salary_to': 350000, 'organization': 'Konig Labs'}
'''
