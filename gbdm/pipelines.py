# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy

class MongoDBPipeline(object):
    def __init__(self):
        client = MongoClient( 'localhost', 27017 )
        self.mongo_base = client.instargam_db
    def process_item(self, item, spider):
        collection = self.mongo_base[type( item ).__name__]
        collection.insert_one(item)
        return item


class GbdmPipeline:
    def process_item(self, item, spider):
        return item
