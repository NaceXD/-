import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = "superjob"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://russia.superjob.ru/vacancy/search/?keywords=python"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath("//span[@class='_38uPK Mx-cr _3wTkb _1fWFN _1R5IY _16BIl _1wutB _2Hujm']//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, responce: HtmlResponse):
        name = responce.xpath("//h1/text()").get()
        url = responce.url
        salary = responce.xpath("//span[@class='_2eYAG _1R5IY _16BIl _2ZnQY']/text()").getall()
        organization = responce.xpath("//span[@class='_1R5IY _16BIl _1wutB _2ZnQY']/text()").get()
        yield JobparserItem(name=name, url=url, salary=salary, organization=organization)
