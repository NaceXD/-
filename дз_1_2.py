import json
import requests
from pprint import pprint

cord = ' 45°02′ северной широты, 38°59′ восточной долготы'
params = {'apikey': '44d6623d-a34a-4807-807a-880a836fc4ce',
            'format': 'json',
            'geocode': cord}
headrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"}

url = 'https://geocode-maps.yandex.ru/1.x/'

response = requests.get(url,headers=headrs, params=params)
resp_j = response.json()
print(f'По координатам {cord} располагается: ')
pprint(resp_j.get('response').get('GeoObjectCollection').get('featureMember')[0].get('GeoObject').get('description'))
pprint(resp_j.get('response').get('GeoObjectCollection').get('featureMember')[0].get('GeoObject').get('name'))

with open('geocoder.txt', 'w') as outfile:
    json.dump(resp_j, outfile)