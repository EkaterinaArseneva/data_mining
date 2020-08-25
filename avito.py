import scrapy
from gbdm.items import GbdmItem

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/novorossiysk/kvartiry/prodam']

    __xpath_query = {
        'pagination': '//div[contains(@data-marker, "pagination-button")]//'
                      'span[@class = "pagination-item-1WyVp"]/text()',
        'ads': '//h3[@class="snippet-title"]/a[@class="snippet-link"][@itemprop="url"]/@href'
    }

    def parse(self, response, start = True):
        if start:
            pages_count = int(response.xpath(self.__xpath_query['pagination']).extract()[-1])
            #pages_count = 2
            for num in range(2, pages_count + 1):
                yield response.follow(
                    f'?p={num}',
                    callback = self.parse,
                    cb_kwargs = {'start': False}
                )

        for link in response.xpath(self.__xpath_query['ads']):
            yield response.follow(
                link,
                callback = self.ads_parse
            )

    def ads_parse(self, response):

        ads_start = '//div[@class = "item-view-content"]'
        header_xpath = ads_start + '//h1[@class="title-info-title"]//span[@class="title-info-title-text"]/text()'
        photo_xpath = ads_start + '//div[@class="gallery-list-wrapper "]//div[@class="gallery-list-item-link"]/img/@src'
        price_xpath = ads_start + '//div[@class="item-price-wrapper"]//span[@class="js-item-price"][@itemprop="price"]'
        address_xpath = ads_start + '//span[@class="item-address__string"]/text()'
        params_xpath = ads_start + '//div[@class="item-params"]//ul[@class="item-params-list"]//li[@class="item-params-list-item"]'

        url = response.url
        title = response.xpath(header_xpath).get()
        photo = response.xpath(photo_xpath).extract()
        price = {response.xpath(price_xpath+'/text()').get().replace(" ", ""):
                     response.xpath(price_xpath+'//..//meta[@itemprop="priceCurrency"]/@content').get()}
        address =  response.xpath(address_xpath).get().replace('\n', '')
        params = []
        for i in range(1, len(response.xpath(params_xpath))+1):
            param_name = response.xpath(params_xpath + f'[{i}]//span[@class="item-params-label"]/text()').get().rstrip()
            if len(response.xpath(params_xpath + f'[{i}]//a/text()')) > 0:
                param_value = max(response.xpath(params_xpath + f'[{i}]//a/text()').getall(), key=len)
            else: param_value = max(response.xpath(params_xpath + f'[{i}]/text()').getall(), key = len)
            param_value = param_value.replace(u'\xa0', u' ').rstrip()
            params.append({'name': param_name,
                           'value': param_value})

        yield GbdmItem(
                title = title,
                url = url,
                address = address,
                photo = photo,
                price = price,
                params = params
        )

        print(1)


