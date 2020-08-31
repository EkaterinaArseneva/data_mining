import scrapy
import json
from scrapy.http.response import Response
from gbdm.items import InstagramPostitem, InstagramOwnerItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    collected_id = {'posts_id': [], 'owners_id': []}
    __login_url = 'https://www.instagram.com/accounts/login/ajax/'
    __tag_url = '/explore/tags/наука/'
    __api_tag_url =  '/graphql/query/'
    __query_hash = "c769cb6c71b24c8a86590b22402fda50"


    def __init__(self, *args, **kwargs):
        self.__login = kwargs['login']
        self.__password = kwargs['password']
        super().__init__(*args, **kwargs)

    def parse(self, response:Response, **kwargs):
        try:
            js_data = self.get_js_shared_data(response)
            print(js_data)
            yield scrapy.FormRequest(self.__login_url,
                                  method='POST',
                                  callback = self.parse,
                                  formdata = {
                                     'username': self.__login,
                                     'enc_password': self.__password
                                  },
                                  headers = {'X-CSRFToken': js_data['config']['csrf_token']}
                                  )
        except AttributeError as e:
            if response.json().get('authenticated'):
                yield response.follow(self.__tag_url, callback = self.tag_page_parse)

    def get_api_url(self, hashtag):
        variables = {
            'tag_name': hashtag['name'],
            'first': 50,
            'after': hashtag['edge_hashtag_to_media']['page_info']['end_cursor']}
        url = f'{self.__api_tag_url}?query_hash={self.__query_hash}&variables={json.dumps( variables )}'
        return url

    def tag_page_parse(self, response: Response):
            js_data = self.get_js_shared_data(response)
            hashtag = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']
            url = self.get_api_url(hashtag)
            yield response.follow(url, callback = self.get_api_hashtag_posts)

    def get_api_hashtag_posts(self, response: Response):
        js_data = json.loads(response.text)
        hashtag = js_data['data']['hashtag']
        posts = hashtag['edge_hashtag_to_media']['edges']

        for post in posts:
            node = post['node']
            node['typename'] = node.pop('__typename')
            if not node['id'] in self.collected_id['posts_id']:
                self.collected_id['posts_id'].append(node['id'])
                if node['edge_liked_by']['count'] > 100 or node['edge_media_to_comment']['count'] > 30:
                    post_url = f'{self.start_urls[0]}p/{node["shortcode"]}/'
                    yield response.follow(post_url, callback=self.get_popular_posts_owners)
                yield InstagramPostitem(node)
        if hashtag['edge_hashtag_to_media']['page_info']['has_next_page']:
            url = self.get_api_url(hashtag)
            yield response.follow(url, callback=self.get_api_hashtag_posts)

    def get_popular_posts_owners(self, response):
        js_data_owner = self.get_js_author_data(response)
        owner = js_data_owner['graphql']['shortcode_media']['owner']
        yield InstagramOwnerItem(owner)



    @staticmethod
    def get_js_shared_data(response):
        marker = 'window._sharedData = '
        data = response.xpath(f'/html/body/script[@type = "text/javascript" and contains(text(), "{marker}")]/text()').get()
        data = data.replace(marker, '')[:-1]
        return json.loads(data)

    @staticmethod
    def get_js_author_data(response):
        marker = "window.__additionalDataLoaded"
        data = response.xpath(f'/html/body/script[@type = "text/javascript" and contains(text(), "{marker}")]/text()').get()
        data = data[48:-2] # не смогла нормально убрать слэши, ни через r, ни через \\
        return json.loads(data)
