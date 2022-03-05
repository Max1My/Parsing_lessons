import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import csv
import re

def split_salary(salary):
    salary_list = []
    print(salary)
    non_fixed_salary = '(^до|^от)'
    result = re.search(non_fixed_salary, salary)
    if result is not None:
        pattern_valute = r'(USD$|руб.$)'
        pattent_salary = r'([0-9]+)'
        min_or_max = re.search(non_fixed_salary,salary)
        valute = re.search(pattern_valute, salary)
        sum = re.search(pattent_salary, salary)
        salary_list.append(min_or_max[0])
        salary_list.append(sum[0])
        salary_list.append(valute[0])
        return salary_list
    else:
        pattern_valute = r'(USD$|руб.$)'
        pattent_salary = r'([0-9]+)'
        valute = re.search(pattern_valute, salary)
        sum = re.findall(pattent_salary,salary)
        salary_list.append(sum[0])
        salary_list.append(sum[1])
        salary_list.append(valute[0])
        return salary_list


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
for article in articles:
    article_data = {}
    vacancy = article.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    link = vacancy['href']
    salary = article.find('span',{'data-qa' :'vacancy-serp__vacancy-compensation'}).getText()
    employer = article.find('a',{'data-qa':'vacancy-serp__vacancy-employer'}).getText()
    address = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).getText()
    # print(f'{vacancy.text} - {salary} - {link} \n'
    #       f' Сайт комании: {base_url} \n'
    #       f' Наименование компании: {employer} \n'
    #       f' Расположение: {address}')
    article_data['vacancy'] = vacancy.text
    # article_data['salary'] = salary.replace(u"\u202f","")
    article_data['salary'] = split_salary(salary.replace(u"\u202f",""))
    article_data['link'] = link
    article_data['employer'] = employer
    article_data['address'] = address
    article_data['from_where'] = base_url
    article_list.append(article_data)

# print(article_list)

with open('hh_ru.json','w',encoding='utf-8') as f:
    json.dump(article_list,f,indent=4,ensure_ascii=False)

with open('hh_ru.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('hh_ru.csv', encoding='utf-8', index=False)