# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            item = self.process_item_hh(item)

        if spider.name == 'superjob':
            item = self.process_item_sj(item)
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print('Такая вакансия уже есть в базе данных')
        return item

    def process_salary_sj(self, salary):
        salary_list = []
        for _ in salary:
            s = _.replace(" ", "").replace("\xa0", "")
            salary_list.append(s)
        salary = salary_list
        return salary

    def process_salary_hh(self, salary):
        hh_list = []
        for _ in salary:
            s = _.replace("", "").replace("\xa0", "")
            hh_list.append(s)
        salary = hh_list
        return salary

    def process_organization(self, organization):
        org_list = []
        for _ in organization:
            o = _.replace("\xa0", "")
            org_list.append(o)
        organization = (' '.join(org_list))
        return organization

    def process_item_hh(self, item):
        if item['salary']:
            item['salary'] = self.process_salary_hh(item['salary'])
            if item['salary'][0] == 'от ':
                item['salary_min'] = int(item['salary'][1])
                if item['salary'][2] == ' до ':
                    item['salary_max'] = int(item['salary'][3])
                    item['currency'] = item['salary'][5]
                else:
                    item['salary_max'] = None
                    item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'до ':
                item['salary_min'] = None
                item['salary_max'] = int(item['salary'][1])
                item['currency'] = item['salary'][3]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None

        del item['salary']
        item['organization'] = self.process_organization(item['organization'])
        item['_id'] = item['url']
        return item

    def process_item_sj(self, item):
        if item['salary']:
            item['salary'] = self.process_salary_sj(item['salary'])
        if item['salary'][0].isdigit():
            item['salary_min'] = int(item['salary'][0])
            item['salary_max'] = int(item['salary'][4])
            item['currency'] = item['salary'][-1]
        elif item['salary'][0] == 'от':
            item['salary_min'] = int(item['salary'][2][:-1])
            item['salary_max'] = None
            item['currency'] = item['salary'][2][-1]
        elif item['salary'][0] == 'до':
            item['salary_min'] = None
            item['salary_max'] = int(item['salary'][2][:-1])
            item['currency'] = item['salary'][2][-1]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None
        del item['salary']
        item['_id'] = item['url']
        del item['url']
        return item
