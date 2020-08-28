# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy import Selector

def get_price(value):
    value = int(value.replace('\u2009', ''))
    return value

def clean_descr(value):
    value = value.replace('\n', '').rstrip().lstrip()
    return value

def get_params(value):
    param_tag = Selector(text=value)
    key = param_tag.xpath('.//div[@class="AdvertSpecs_label__2JHnS"]/text()').get()
    way_a = param_tag.xpath('.//a/text()').get()
    way_div = param_tag.xpath('.//div[@class = "AdvertSpecs_data__xK2Qx"]/text()').get()
    if way_a: value = way_a
    else: value =  way_div

    return key, value

class YoulaItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor = TakeFirst())
    holder_url = scrapy.Field()
    descr = scrapy.Field(input_processor = MapCompose(clean_descr), output_processor = TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor = TakeFirst())
    params = scrapy.Field(output_processor = lambda x: dict(get_params(itm) for itm in x))
    url = scrapy.Field(output_processor = TakeFirst())
    pass

