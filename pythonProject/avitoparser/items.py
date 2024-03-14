# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose, MapCompose



class AvitoparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose())
    price = scrapy.Field(input_processor=Compose(), output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())

    # name = scrapy.Field()
    # photos = scrapy.Field()
    # price = scrapy.Field()
    # description = scrapy.Field()
    # url = scrapy.Field()scrapy.Field()