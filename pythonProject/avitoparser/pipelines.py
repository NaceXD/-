# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for photo in item['photos']:
                try:
                    yield scrapy.Request(photo)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class AvitoparserPipeline:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.mongo_db = client.avitoparser

    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print('Такая товар уже есть в базе данных')
        return item
