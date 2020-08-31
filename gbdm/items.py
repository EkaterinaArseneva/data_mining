# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy import Selector
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

def validate_photo(value):
    if value[:2] == '//':
        return f'https:{value}'
    return value

def validate_prices(value):

    print(1)
class AvitoItem(scrapy.Item):
    _id = scrapy.Field(output_processor = TakeFirst())
    title = scrapy.Field()
    url = scrapy.Field(output_processor = TakeFirst())
    address = scrapy.Field(output_processor = TakeFirst())
    photo = scrapy.Field(input_processor = MapCompose(validate_photo))
    price = scrapy.Field()
    params = scrapy.Field()
    pass

class InstagramPostitem(scrapy.Item):
    _id = scrapy.Field()
    comments_disabled = scrapy.Field()
    typename = scrapy.Field()
    id = scrapy.Field()
    edge_media_to_caption = scrapy.Field()
    shortcode = scrapy.Field()
    edge_media_to_comment = scrapy.Field()
    taken_at_timestamp = scrapy.Field()
    dimensions = scrapy.Field()
    display_url = scrapy.Field()
    edge_liked_by = scrapy.Field()
    edge_media_preview_like = scrapy.Field()
    owner = scrapy.Field()
    thumbnail_src = scrapy.Field()
    thumbnail_resources = scrapy.Field()
    is_video = scrapy.Field()
    accessibility_caption = scrapy.Field()
    __len__ = scrapy.Field()
    product_type = scrapy.Field()
    video_view_count = scrapy.Field()

class InstagramOwnerItem(scrapy.Item):
    _id = scrapy.Field()
    id = scrapy.Field()
    is_verified = scrapy.Field()
    profile_pic_url = scrapy.Field()
    username = scrapy.Field()
    blocked_by_viewer = scrapy.Field()
    restricted_by_viewer = scrapy.Field()
    followed_by_viewer = scrapy.Field()
    full_name = scrapy.Field()
    has_blocked_viewer = scrapy.Field()
    is_private = scrapy.Field()
    is_unpublished = scrapy.Field()
    requested_by_viewer = scrapy.Field()
    edge_owner_to_timeline_media = scrapy.Field()
    edge_followed_by = scrapy.Field()
    __len__ = scrapy.Field()
    pass