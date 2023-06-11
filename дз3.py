import json
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError

with open('data.json') as j:
    vacancy = json.load(j)

client = MongoClient('localhost', 27017)

db = client['вакансии']
python = db.python

for i in vacancy:
    name = i['name']
    linc = i['link']
    site = i['job site']
    organization = i['organization']
    if i['salary'] == None:
        doc = {
            '_id': linc,
            'Название': name,
            'Сайт': site,
            'Организация': organization,
            'Зарпала': 'Не указано'
        }
        try:
            python.insert_one(doc)
        except DuplicateKeyError:
            print('Такая вакансия уже есть в базе данных')
    else:
        for key in i['salary']:
            if key == 'minimum' and 'currency':
                currency = i['salary']['currency']
                minimum = i['salary']['minimum']
                doc = {
                    '_id': linc,
                    'Название': name,
                    'Сайт': site,
                    'Организация': organization,
                    'Зарплата от': minimum,
                    'Валюта': currency
                }
                try:
                    python.insert_one(doc)
                except DuplicateKeyError:
                    print('Такая вакансия уже есть в базе данных')
            elif key == 'maximum' and 'currency':
                currency = i['salary']['currency']
                maximum = i['salary']['maximum']
                doc = {
                    '_id': linc,
                    'Название': name,
                    'Сайт': site,
                    'Организация': organization,
                    'Зарплата до': maximum,
                    'Валюта': currency
                }
                try:
                    python.insert_one(doc)
                except DuplicateKeyError:
                    print('Такая вакансия уже есть в базе данных')
            elif key == 'minimum' and 'maximum' and 'currency':
                minimum = i['salary']['minimum']
                currency = i['salary']['currency']
                maximum = i['salary']['maximum']
                doc = {
                    '_id': linc,
                    'Название': name,
                    'Сайт': site,
                    'Организация': organization,
                    'Зарплата от': minimum,
                    'Зарплата до': maximum,
                    'Валюта': currency
                }
                try:
                    python.insert_one(doc)
                except DuplicateKeyError:
                    print('Такая вакансия уже есть в базе данных')


def salary_finder():
    s = int(input('Введите минимальную зарплату: '))

    vacancies_answer = []
    for a in python.find({'$or': [{'Зарплата от': {'$gt': s}}, {'Запрплата до': {'$gt': s}}]}):
        vacancies_answer.append(a)

    return vacancies_answer

pprint(salary_finder())