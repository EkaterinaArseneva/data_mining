"""Источник: https://5ka.ru/special_offers/

Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы

результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются
в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать товары
исключительно соответсвующие данной категории.

пример структуры данных для файла:

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT},  {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}"""

import requests
import time
import json
import csv

"""
domain = 'https://5ka.ru'
_api_path = '/api/v2/special_offers/'
_api_path_cat = '/api/v2/categories/'
#_api_path = '/special_offers/'

url = domain + _api_path
url_cat = domain + _api_path_cat
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
}
params = {'store': '',
        'records_per_page': 12,
        'page': 1,
        'categories': '',#732 = безалкогольные напитки
        'ordering': '',
        'price_promo__gte': '',
        'price_promo__lte': '',
        'search': ''
          }
response = requests.get(url, headers=headers, params=params)
params0 = params
params0['categories'] = 732
print(params0)
response0 = requests.get(url, headers=headers, params=params0)
print(response0.json())
categories = requests.get(url_cat, params=headers).json()
print(categories)
"""


# print(response.json())
# with open('test.html', 'w', encoding='utf8') as file:
# file.write(response.text)
# print(1)

class Parser5ka:
    _domain = 'https://5ka.ru'
    _api_path = '/api/v2/special_offers/'
    params = {
        'records_per_page': 20,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    def __init__(self):
        self.products = []

    def download(self):
        params = self.params
        url = self._domain + self._api_path

        while url:
            response = requests.get( url, headers=self.headers, params=params )
            # todo сделать проверку что прилетел json
            data = response.json()
            params = {}
            url = data['next']
            self.products.extend( data['results'] )
            time.sleep( 0.1 )

    def category_load(self):
        url = self._domain + self._api_path
        api_path_cat = '/api/v2/categories/'
        url_cat = self._domain + api_path_cat
        params_cat = self.params
        categories = requests.get( url_cat, headers=self.headers, params=self.params ).json()
        products_cat = []

        for category in categories:
            params_cat['category'] = category['parent_group_code']

            while url:
                response_cat = requests.get(url, headers=self.headers, params=params_cat )
                data_cat = response_cat.json()
                url = data_cat['next']
                products_cat.extend( data_cat['results'] )
                time.sleep( 0.1 )
            with open(category['parent_group_name'] + '.txt', 'w', encoding='utf8') as f:
                json.dump({'name': category['parent_group_name'], 'code': category['parent_group_code'],
                            'products': products_cat}, f )


parser = Parser5ka()
parser.category_load()

