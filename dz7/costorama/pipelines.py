# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class CostoramaPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.castorama

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['designation'] = self.process_designation(item['designation'])
        specifications_dikt = dict(zip(item['designation'], item['meaning']))
        item['specifications'] = specifications_dikt
        del item['designation']
        del item['meaning']
        item['_id'] = item['url']
        del item['url']
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print('Такая товар уже есть в базе данных')
        return item

    def process_designation(self, designation):
        des_list = []
        for x in designation:
            if x != '':
                des_list.append(x)
        designation = des_list
        return designation


class CostoramaPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        photos_to_dowland = []
        for photo in item['photos']:
            photos = 'https://www.castorama.ru' + photo
            photos_to_dowland.append(photos)
        for img in photos_to_dowland:
            try:
                yield scrapy.Request(img)
            except Exception as e:
                print(e)

    def item_completed(self, result, item, info):
        if result:
            item['photos'] = [itm[1] for itm in result if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        fold = f"{item['name']}/"
        return fold + super().file_path(request, response=response, info=info, item=item)
