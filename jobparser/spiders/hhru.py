import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://krasnodar.hh.ru/search/vacancy?text=python"]

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, responce: HtmlResponse):
        name = responce.xpath("//h1[@data-qa='vacancy-title']/text()").get()
        url = responce.url
        salary = responce.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        organization = responce.xpath("//div[@data-qa= 'vacancy-company__details']//text()").getall()
        yield JobparserItem(name=name, url=url, salary=salary, organization=organization)
