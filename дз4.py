from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

url = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
news_list = []
# Получаем и обрабатываем главную новость (она же большая)
b_news = {}
dom.xpath("//a[contains(@class, 'card-big _topnews _news')]")
b_name = dom.xpath(".//h3[@class='card-big__title']/text()")
b_link = dom.xpath(".//a[@class='card-big _topnews _news']/@href")
b_n_time = dom.xpath(".//time[@class='card-big__date']/text()")
_, _, year, month, day, *_ = b_link[0].split('/')
b_news['name'] = b_name[0]
b_news['link'] = url + b_link[0]
b_news['website'] = 'lenta'
b_news['date'] = f'{year}-{month}-{day}-{b_n_time[0]}'
news_list.append(b_news)
# Получаем и обрабатываем остальные новости
items = dom.xpath("//a[contains(@class, 'card-mini _topnews')]")
for item in items:

    news = {}

    name = item.xpath(".//span[@class='card-mini__title']/text()")
    link = item.xpath(".//@href")

    # название источника;
    news['website'] = 'lenta'
    # наименование новости;
    news['name'] = name[0]
    # ссылка на новость;
    news['link'] = url + link[0]
    # дата публикации (из ссылки)
    n_time = item.xpath(".//time[@class='card-mini__date']/text()")
    _, _, year, month, day, *_ = link[0].split('/')
    news['date'] = f'{year}-{month}-{day}-{n_time[0]}'
    news_list.append(news)

pprint(news_list)

client = MongoClient('localhost', 27017)

db = client['новости']
lenta = db.lenta

for news in news_list:
    doc = {
        '_id': news['link'],
        'Название': news['name'],
        'Сайт': news['website'],
        'Дата публикации': news['date']
    }
    try:
        lenta.insert_one(doc)
    except DuplicateKeyError:
        print('Такая вакансия уже есть в базе данных')