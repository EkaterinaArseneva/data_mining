import scrapy
from scrapy.selector import Selector
from youla.items import YoulaItem
from scrapy.loader import ItemLoader

class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/moskva/cars/used/volvo']

    __xpath_query = {
        'pagination': '//div[@class = "Paginator_block__2XAPy app_roundedBlockWithShadow__1rh6w"]//'
                      'div[@class = "Paginator_total__oFW1n"]/text()',
        'ads': '//div[@class="SerpSnippet_titleWrapper__38bZM"]//a[@data-target="serp-snippet-title"]/@href',
        'title': '//div[@class="AdvertCard_topAdvertHeader__iqqNl"]//div[@class="AdvertCard_advertTitle__1S1Ak"]/text()',
        'params': '//div[@class ="AdvertCard_specs__2FEHc"]//div[@class="AdvertSpecs_row__ljPcX"]',
        'descr': '//div[@class = "AdvertCard_descriptionInner__KnuRi"]/text()',
        'price': '//div[@class = "AdvertCardStickyContacts_toolbar__pMpq1"]//div[@class]/text()',
        'holder_url' : '//a[@class = "SellerInfo_name__3Iz2N"]/@href',
        'photos': '//figure[@class = "PhotoGallery_photo__36e_r"]//picture//img/@src'
    }


    def parse(self, response, start=True):
        if start:
            total_pages = response.xpath(self.__xpath_query['pagination'] ).extract()
            pages_count = int(list(filter(lambda x: x.isdigit(), total_pages))[0])
            print(pages_count)
            # pages_count = 2
            for num in range(2, pages_count + 1 ):
                yield response.follow(
                    f'/moskva/cars/used/volvo/?page={num}#serp',
                    callback=self.parse,
                    cb_kwargs={'start': False}
                )

        for link in response.xpath(self.__xpath_query['ads']).extract():
            yield response.follow(
                link,
                callback=self.ads_parse
            )

    def ads_parse(self, response):
        item_loader = ItemLoader(YoulaItem(), response)
        for key, value in self.__xpath_query.items():
            if key in ('pagination', 'ads'):
                continue
            item_loader.add_xpath(key, value)
        item_loader.add_value('url', response.url)

        yield item_loader.load_item()