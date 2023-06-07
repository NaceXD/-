from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint


vacancy = input('Введите вакансию: ')
url = 'https://hh.ru/search/vacancy'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"}
params = {'search_field': 'name', 'text': vacancy, 'page': 0}
job_list = []

while True:
    session = requests.Session()
    response = session.get(url, headers=headers, params=params)
    if response.status_code >= 400:
        break
    dom = BeautifulSoup(response.text, 'html.parser')
    job_openings = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
    if len(job_openings) == 0:
        break
    else:
        for job in job_openings:
            job_data = {}
            tag_a = job.find('a', {'class': 'serp-item__title'})
            job_link = tag_a.get('href')
            job_name = tag_a.text
            organization = job.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).text
            salary = job.find('span', {'class': 'bloko-header-section-3'})
            if salary:
                salary = salary.text
            job_data['name'] = job_name
            job_data['link'] = job_link
            job_data['job site'] = 'hh.ru'
            job_data['organization'] = organization
            salary_data = {}
            salary_value = (str(salary)).replace('\u202f', '')
            if salary_value[0].isdigit():
                re_min_max = re.compile(r'\d+')
                re_currency = re.compile(r'\w+')
                minimum = re_min_max.findall(salary_value)[0]
                maximum = re_min_max.findall(salary_value)[1]
                currency = re_currency.findall(salary_value)[-1]
                salary_data['min'] = int(minimum)
                salary_data['max'] = int(maximum)
                salary_data['currency'] = currency
                job_data['salary'] = salary_data
            elif salary_value[0] == 'о':
                re_min_max = re.compile(r'\d+')
                re_currency = re.compile(r'\w+')
                minimum = re_min_max.findall(salary_value)[0]
                currency = re_currency.findall(salary_value)[-1]
                salary_data['min'] = int(minimum)
                salary_data['currency'] = currency
                job_data['salary'] = salary_data
            elif salary_value[0] == 'д':
                re_min_max = re.compile(r'\d+')
                re_currency = re.compile(r'\w+')
                maximum = re_min_max.findall(salary_value)[0]
                currency = re_currency.findall(salary_value)[-1]
                salary_data['max'] = int(maximum)
                salary_data['currency'] = currency
                job_data['salary'] = salary_data
            else:
                job_data['salary'] = None
            job_list.append(job_data)
        params['page'] += 1

print(f'На сайте hh.ru по запросу {vacancy} найдено {len(job_list)} вакансий')
pprint(job_list)
