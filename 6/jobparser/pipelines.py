# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_hh_sj

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]

        if not collection.find_one({'_id': item['_id']}):
            collection.insert_one(item)

        return item
