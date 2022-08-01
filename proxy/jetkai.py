import json

import requests

from bs4 import BeautifulSoup as bs
from utils import Logger

logger = Logger.get_logger(__name__)

url = 'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies.json'

logger.info('get proxy from GH jetkai')
list_proxies = []

content = requests.get(url).content.decode('utf8')
logger.info('get done')

proxies = json.loads(content)
logger.info('format list')
for item_schema in proxies:
    for item in proxies.get(item_schema):
        list_proxies.append({'proxy': item})
logger.info(f'Обнаружено прокси - {len(list_proxies)}:')

__all__ = ['list_proxies']
