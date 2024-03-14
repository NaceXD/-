import scrapy
from scrapy_splash import SplashRequest
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.start_urls = [f"https://www.avito.ru/all?p={self.page}&q={kwargs.get('request')}"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url)

    def parse(self, response):
        links = response.xpath("//a[@data-marker='item-title']/@href").getall()
        for link in links:
            yield SplashRequest("https://avito.ru/" + link, callback=self.parse_ads)

    def parse_ads(self, response):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('name', "//span[@class='title-info-title-text']/text()")
        loader.add_xpath('photos', "//div[@data-marker='image-frame/image-wrapper']/img/@src |"
                                   "//img/@src")
        loader.add_xpath('price', "//span[@itemprop='price']/@content")
        loader.add_xpath('description', "//div[@data-marker='item-view/item-description']/p/text()")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//span[@class='title-info-title-text']/text()").get()
        # photos = response.xpath("//div[@data-marker='image-frame/image-wrapper']/img/@src |"
        #                          "//img/@src").getall()
        # price = response.xpath("//span[@itemprop='price']/@content").get()
        # description = response.xpath("//div[@data-marker='item-view/item-description']/p/text()").get()
        # url = response.url
        # yield AvitoparserItem(name=name, photos=photos, price=price, description=description, url=url)
