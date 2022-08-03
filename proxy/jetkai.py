import json

import requests

from bs4 import BeautifulSoup as bs
from sqlalchemy.sql.functions import now

from utils import Logger

logger = Logger.get_logger(__name__)

url = 'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies.json'

logger.debug('get proxy from GH jetkai')
list_proxies = []

content = requests.get(url).content.decode('utf8')
logger.debug('get done')

proxies = json.loads(content)
logger.debug('format list')
for item_schema in proxies:
    for item in proxies.get(item_schema):
        list_proxies.append({'proxy': item, 'import_at': now()})
logger.info(f'Обнаружено прокси - {len(list_proxies)}:')

__all__ = ['list_proxies']
