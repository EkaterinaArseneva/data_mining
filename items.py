# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GbdmItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    photo = scrapy.Field()
    price = scrapy.Field()
    params = scrapy.Field()
    pass
