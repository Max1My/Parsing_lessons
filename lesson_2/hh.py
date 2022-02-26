import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json
import csv

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
    article_data['salary'] = salary
    article_data['link'] = link
    article_data['employer'] = employer
    article_data['address'] = address
    article_data['from_where'] = base_url
    article_list.append(article_data)

# print(article_list)

with open('hh_ru.json','w',encoding='utf-8-sig') as f:
    json.dump(article_list,f,indent=4,ensure_ascii=False)

with open('hh_ru.json', encoding='utf-8-sig') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('hh_ru.csv', encoding='utf-8', index=False)