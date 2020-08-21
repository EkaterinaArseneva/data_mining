
"""
Источник habr.ru
задача обойти ленту статей (лучшее за сутки) извлеч данные

заголовок
url статьи
имя автора
ссылка на автора
список тегов ( имя тега и url)
список хабов (имя и url)
спроектировать sql базу данных таким образом
что-бы данные о тегах хабах и авторах были атомарны, и не дублировались в БД
"""

import re
from requests.auth import HTTPProxyAuth

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from pymongo import MongoClient
import re
import datetime as dt
import time


class HabrParser:
    domain = 'https://habr.com'
    start_url = 'https://habr.com/ru/top/daily'

    def __init__(self):
        self.visited_urls = set()
        self.post_links = set()
        self.posts_data = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
    def parse_rows(self, url = start_url):
        while url:
            if url in self.visited_urls:
                break

            response = requests.get(url, headers = self.headers)
            time.sleep(0.01)
            self.visited_urls.add(url)
            soup = BeautifulSoup(response.text, 'lxml')
            url = self.get_next_page(soup)
            self.search_post_links(soup)

    def get_next_page(self, soup: BeautifulSoup) -> str:
        ul = soup.find('ul', attrs = {'class': 'arrows-pagination'})
        a = ul.find('a', attrs = {'id': 'next_page'})
        next_page_link = f'{self.domain}{a.get("href")}' if a and a.get("href") else None
        return next_page_link

    def search_post_links(self, soup: BeautifulSoup) -> List[str]:
        posts_list = soup.find('div', attrs = {'class': 'posts_list'})
        posts = posts_list.find_all('article', attrs = {'class': 'post_preview'})
        links = {item.find("a", attrs = {"class": "post__title_link"}).get("href") for item in posts}
        self.post_links.update(links)


    def post_page_parse(self):

        for url in list(self.post_links):
            if url in self.visited_urls:
                continue
            response = requests.get( url, headers=self.headers )
            time.sleep(1)
            while response.status_code != 200:
                response = requests.get( url, headers=self.headers )
            soup = BeautifulSoup(response.text, 'lxml')
            self.visited_urls.add( url )

            pd = {}
            pd['url'] = url
            pd.update(self.get_post_data(soup))
            self.posts_data.append(pd)

    def get_post_data(self, soup: BeautifulSoup):

        result = {}
        #total blocks
        wrapper = soup.find('div', attrs = {'class': {'post_wrapper', 'post__wrapper'}})
        author_block = soup.find( 'div', attrs={'class': 'author-panel'})
        tags_block = wrapper.find( 'dl', attrs={'class': 'post__tags'})
        hubs_block = wrapper.find( 'dl', attrs={'class': 'post__tags'} )

        #title
        result['title'] = wrapper.find('span', attrs={'class': 'post__title-text'}).text
        #author
        author_block_spec = author_block.find( 'div', attrs={'class': 'user-info__about'} )
        author_info = author_block_spec.find('a', attrs={'class': 'user-info__fullname'})
        if not author_info:
            author_info = author_block_spec.find('a', attrs={'class': 'user-info__nickname'})
        result['author'] = author_info.text
        result['author_url'] = author_info.get('href')

        #tags
        tags_block_spec = tags_block.find('dd', attrs={'class': 'post__tags-list'})
        tags_info = tags_block_spec.find_all('li', attrs={'class': 'inline-list__item_tag'})
        tags = set((tag.find('a', attrs = {'class': 'post__tag', 'rel': 'tag'}).text,
                 tag.find('a', attrs = {'class': 'post__tag', 'rel': 'tag'}).get("href"))
                  for tag in tags_info)
        result['tags'] = tags

        #hubs
        hubs_block_spec = hubs_block.find_next('dd', attrs={'class': 'post__tags-list'})
        hubs_info = hubs_block_spec.find_all('li', attrs={'class': 'inline-list__item_tag'})
        hubs = set((hub.find('a', attrs={'class': 'post__tag', 'rel': 'tag'}).text,
                 hub.find('a', attrs={'class': 'post__tag', 'rel': 'tag'}).get("href"))
                for hub in hubs_info)
        result['hubs'] = hubs
        return result

    def parse(self):
        self.parse_rows()
        self.post_page_parse()

if __name__ == '__main__':
    parser = HabrParser()
    parser.parse()

