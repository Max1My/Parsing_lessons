import re
import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup


from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

base_url = 'https://hh.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
position = input('Какую должность искать?: ')
params = {
    'only_with_salary':'true',
    'clusters': 'true',
    'area': '1',
    'ored_clusters': 'true',
    'enable_snippets': 'true',
    'text': position
}

url = f'{base_url}/search/vacancy'
response = requests.get(url, headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')

articles = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})

article_list = []

client = MongoClient('127.0.0.1', 27017)

db = client['vacancy']
hh_ru = db.hh_ru

def split_salary(salary):
    salary_list = []
    # print(salary)
    non_fixed_salary = '(^до|^от)'
    result = re.search(non_fixed_salary, salary)
    if result is not None:
        pattern_valute = r'(USD$|руб.$|EUR$)'
        pattent_salary = r'([0-9]+)'
        min_or_max = re.search(non_fixed_salary,salary)
        valute = re.search(pattern_valute, salary)
        sum = re.search(pattent_salary, salary)
        salary_list.append(min_or_max[0])
        salary_list.append(int(sum[0]))
        salary_list.append(valute[0])
        return salary_list
    else:
        pattern_valute = r'(USD$|руб.$|EUR$)'
        pattent_salary = r'([0-9]+)'
        valute = re.search(pattern_valute, salary)
        sum = re.findall(pattent_salary,salary)
        salary_list.append(int(sum[0]))
        salary_list.append(int(sum[1]))
        salary_list.append(valute[0])
        return salary_list

def search_vacancy(salary):
    for doc in hh_ru.find({'salary': {'$gt': [salary]}}):
        pprint(doc)

def get_id(link):
    id_vacancy = r'([0-9]+)'
    _id = re.search(id_vacancy,link)
    return _id[0]

for article in articles:
    vacancy = article.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    link = vacancy['href']
    salary = article.find('span',{'data-qa' :'vacancy-serp__vacancy-compensation'}).getText()
    employer = article.find('a',{'data-qa':'vacancy-serp__vacancy-employer'}).getText()
    address = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).getText()
    try:
        hh_ru.insert_one({"_id": get_id(link),
                            "vacancy": vacancy.text,
                            "salary": split_salary(salary.replace(u"\u202f","")),
                            "link": link,
                            "employer": employer.replace(u"\xa0"," "),
                            "address": address.replace(u"\xa0"," "),
                            "from_where": base_url
                          })
    except DuplicateKeyError:
        print('Document is already exist')


# Проверка дублирования записи
# for doc in hh_ru.find({'_id': '53427547'}):
#     pprint(doc)

# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты)

search_vacancy(int(input('Вакансии с какой зарплатой искать?: ')))
