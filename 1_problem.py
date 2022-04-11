from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import os.path
import json


def save_html():
    search_word = input("Какие вакансии вас интересуют: ").replace(' ', "+")

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

    i = 0
    response = True
    while response:
        url = f'https://hh.ru/search/vacancy?text={search_word}&page={i}'
        src = requests.get(url, headers=headers)
        response = bool(requests.get(url))
        i += 1

    with open(f"html\page_{i}.html", 'w', encoding='utf-8') as f:
        f.write(src.text)

def get_info():
    i = 0
    vacancy_list = []
    path = 'html'
    num_files = len([f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))])
    print(num_files)
    for i in range(num_files):
        with open(f"html\page_{i}.html", 'r', encoding='utf-8') as f:
            src = f.read()
            dom = bs(src, 'html.parser')
            vacancies = dom.find_all("div", {"class": "vacancy-serp-item"})
            for vacancy in vacancies:
                vacancy_info = {}
                try:
                    name = vacancy.find('a', {"data-qa": "vacancy-serp__vacancy-title"}).text
                except AttributeError:
                    name = None
                try:
                    href = vacancy.find('a', {"data-qa": "vacancy-serp__vacancy-title"})['href']
                except TypeError:
                    href = None
                try:
                    salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text
                except AttributeError:
                    salary = None
                if salary == None:
                    min_salary = None
                    max_salary = None
                    currency = None
                elif '–' in salary:
                    salary_list = salary[0:-4].split('–')
                    min_salary = salary_list[0].replace(' ', '')
                    max_salary = salary_list[1].replace(' ', '')
                    currency = salary[-4:].replace('.', '').replace(' ', '')
                elif 'от' in salary:
                    min_salary = salary[2:-4].strip()
                    max_salary = None
                    currency = salary[-4:].replace('.', '').replace(' ', '')
                elif 'до' in salary:
                    min_salary = None
                    max_salary = salary[2:-4].strip()
                    currency = salary[-4:].replace('.', '').replace(' ', '')
                vacancy_info['name'] = name
                vacancy_info['href'] = href
                vacancy_info['min_salary'] = min_salary
                vacancy_info['max_salary'] = max_salary
                vacancy_info['currency'] = currency
                vacancy_list.append(vacancy_info)
                i += 1
    return vacancy_list


def save_json(list):
    with open("response.json", "w", encoding='utf-8') as file:
        json.dump(list, file, indent=4, ensure_ascii=False)


save_json(get_info())
# pprint(vacancy_list)
