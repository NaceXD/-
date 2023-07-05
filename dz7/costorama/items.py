# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def clean_price(value):
    new_value = value.replace(' ', '').replace('\n', '')
    try:
        new_value = int(new_value)
    except:
        pass
    return new_value


def clean_name(value):
    new_value = value.replace('\n', '').replace(' ', '')
    # new_value = value.replace(' ', '') Но тогда будут большие пробелы до и после названия
    return new_value


def clean_designation(value):
    new_value = value.replace('\n', '').replace(' ', '')
    return new_value


def clean_meaning(value):
    new_value = value.replace('\n', '').replace(' ', '')
    return new_value


class CostoramaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_name))
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_price))
    photos = scrapy.Field()
    designation = scrapy.Field(input_processor=MapCompose(clean_designation))
    meaning = scrapy.Field(input_processor=MapCompose(clean_meaning))
    specifications = scrapy.Field()
    _id = scrapy.Field()
