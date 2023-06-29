import scrapy
from costorama.items import CostoramaItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = "castorama"
    allowed_domains = ["castorama.ru"]
    start_urls = ["https://www.castorama.ru/bytovaja-tehnika/phones-and-audio/?PAGEN_3=1"]

    def parse(self, response):
        links = response.xpath("//a[@class='product-card__img-link']/@href")
        for link in links:
            yield response.follow(link, callback=self.product_parse)
        next_page = response.xpath("//a[@class='next i-next']/@href")
        if next_page:
            yield response.follow(link, callback=self.parse)

    def product_parse(self, response):
        loader = ItemLoader(item=CostoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='regular-price']//text()")
        loader.add_xpath('photos', "//img[@class='top-slide__img swiper-lazy']/@data-src")
        loader.add_xpath('designation',
                         "//div[@id='specifications']//dt[@class='specs-table__attribute-label _first']//text()")
        loader.add_xpath('meaning',
                         "//div[@id='specifications']//dd[@class='specs-table__attribute-value _first']/text()")
        loader.add_value('url', response.url)
        # name = response.xpath("//h1/text()").get()
        # url = response.url
        # price = response.xpath("//span[@class='regular-price']//text()").getall()
        # photos = response.xpath("//img[@class='top-slide__img swiper-lazy']/@data-src").getall()
        # designation = response.xpath("//dt[@class='specs-table__attribute-label _first']//text()").getall()
        # meaning = response.xpath("//dd[@class='specs-table__attribute-value _first']/text()").getall()
        yield loader.load_item()
