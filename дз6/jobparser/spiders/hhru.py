import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem



class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    search = 'python'
    start_urls = [
        f'https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={search}&showClusters=true']

    def parse(self, response: HtmlResponse):  # С этого метода все и начинается (в response - первый ответ)
        # Ищем ссылку для перехода на следующую страницу
        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()
        # Ищем на полученной странице ссылки на вакансии
        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:  # Перебираем ссылки
            yield response.follow(link, callback=self.vacancy_parse)
            # Переходим по каждой ссылке и обрабатываем ответ методом vacancy_parse
            yield response.follow(next_page, callback=self.parse)
            # Переходим по ссылке на следующую страницу и возвращаемся к началу метода parse

    def vacancy_parse(self, response: HtmlResponse):  # Здесь обрабатываем информацию по вакансии
        name_job = response.xpath('//h1/text()').extract_first()  # Получаем наименование вакансии
        salary_job = response.css(
            'p.vacancy-salary span::text').extract()  # Получаем зарплату в виде списка отдельных блоков
        location_job = response.xpath('//p[@data-qa="vacancy-view-location"]//text()').extract()
        position_link = response.url
        company_job = response.xpath('//span[@class="bloko-section-header-2 bloko-section-header-2_lite"]/text()').extract()
        yield JobparserItem(name=name_job, salary=salary_job, location=location_job, link=position_link, company=company_job)  # Передаем данные в item для создания структуры json