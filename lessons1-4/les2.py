import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from pymongo import MongoClient
import re
import datetime as dt

class GBBlogParse:
    domain = 'https://geekbrains.ru'
    start_url = 'https://geekbrains.ru/posts'

    def __init__(self):
        self.visited_urls = set()
        self.post_links = set()
        self.posts_data = []
        self.client = MongoClient()
        self.db = self.client['parse_GB']
        self.collection = self.db['posts']

    # todo обход ленты по пагинации
    def parse_rows(self, url = start_url):
        while url:
            if url in self.visited_urls:
                break
            response = requests.get(url)
            self.visited_urls.add(url)
            soup = BeautifulSoup(response.text, 'lxml')
            url = self.get_next_page(soup)
            self.search_post_links(soup)

    def get_next_page(self, soup: BeautifulSoup) -> str:
        ul = soup.find('ul', attrs = {'class': 'gb__pagination'})
        a = ul.find('a', text = re.compile('›'))
        return f'{self.domain}{a.get("href")}' if a and a.get("href") else None

    def search_post_links(self, soup: BeautifulSoup) -> List[str]:
        wrapper = soup.find('div', attrs = {'class': 'post-items-wrapper'})
        posts = wrapper.find_all('div', attrs = {'class': 'post-item'})
        print(posts)
        links = {f'{self.domain}{item.find("a").get("href")}' for item in posts}
        self.post_links.update(links)
"""
    def post_page_parse(self):

        for url in list(self.post_links)[:5]:
            if url in self.visited_urls:
                continue
            response = requests.get(url)
            self.visited_urls.add(url)
            soup = BeautifulSoup(response.text, 'lxml')

            pd = {}
            pd['url'] = url
            pd.update(self.get_post_data(soup))

            self.posts_data.append(pd)

    def get_post_data(self, soup: BeautifulSoup):
        result = {}

        result['title'] = soup.find( 'h1', attrs={'class': 'blogpost-title'} ).text

        content = soup.find('div', attrs={'class': 'page-content'})
        post_data = content.find('div', attrs = {'class': 'blogpost-content', 'itemprop': 'articleBody'})
        img = post_data.find( 'img' )
        result['image'] = img.get( 'src' ) if img else None

        author_info = soup.find('div', attrs = {'itemprop':"author"})
        result['writer_name'] = author_info.text
        result['writer_url'] = self.domain + author_info.findParent().get("href")

        post_date_info = content.find('div', attrs = {'class': 'blogpost-date-views'})
        date = post_date_info.find('time', attrs = {'itemprop': "datePublished"})
        result['pub_date'] = dt.datetime.fromisoformat(date.get('datetime'))

        return result

    def save_to_mongo(self):
       self.collection.insert_many(self.posts_data)


    def get_data_from_mongo(self, start_date = input('Start date (yyyy-mm-dd): ' ), end_date = input('End date (yyyy-mm-dd): ' )):
        if not start_date:
            start_date = dt.datetime(1,1,1, tzinfo=dt.timezone.utc)
        else:
            start_date = dt.datetime.fromisoformat(start_date)
            start_date = start_date.replace(tzinfo=dt.timezone.utc)
        if not end_date:
            end_date = dt.datetime.now(tz=dt.timezone.utc)
        else:
            end_date = dt.datetime.fromisoformat(end_date)
            end_date = end_date.replace(tzinfo=dt.timezone.utc)
        filtered_posts_data = list(self.collection.find({'$and':[{'pub_date': {'$gte': start_date}},
                                                                      {'pub_date': {'$lte': end_date}}]}))
        print(filtered_posts_data)




"""
if __name__ == '__main__':
    parser = GBBlogParse()
    parser.parse_rows()
#    parser.post_page_parse()
#    parser.save_to_mongo()

#    parser.get_data_from_mongo()
