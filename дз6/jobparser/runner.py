from scrapy.crawler import CrawlerProcess           # Импортируем класс для создания процесса
from scrapy.settings import Settings                # Импортируем класс для настроек

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    crawler_settings = Settings()                   # Создаем объект с настройками
    crawler_settings.setmodule(settings)            # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)     # Создаем объект процесса для работы
    process.crawl(HhruSpider)                               # Добавляем нашего паука
    process.crawl(SuperjobSpider)

    process.start()