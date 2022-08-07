from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup as bs
from sqlalchemy.sql.functions import now

from utils import Logger, get_page

logger = Logger.get_logger(__name__)

base_url = 'https://freeproxylist.ru/'


def find_last_page(soup):
    logger.debug('find last page')
    query = soup.find_all("li", attrs={"page-item"})[-1:][0].find('a', href=True)['href']
    parsed_url = urlparse(base_url + query)
    captured_value = parse_qs(parsed_url.query).get('page')[0]
    return captured_value


def parse_proxies(soup):
    proxies = []
    for row in soup.find("tbody", attrs={"class": "table-proxy-list"}).find_all("tr"):
        try:
            ip = row.find('th').text.strip()
            port = row.find_all("td")[0].text.strip()
            host = f"{ip}:{port}"
            proxies.append({'proxy': host, 'import_at': now()})
        except IndexError:
            continue
    return proxies


def get_free_proxies():
    logger.debug('get proxy from freeproxylist.ru')
    soup = bs(get_page(base_url).content, "html.parser")
    last_page = int(find_last_page(soup))
    logger.debug('last page = ' + str(last_page))
    proxies = parse_proxies(soup)

    for i in range(last_page):
        logger.debug(f'parse page {i + 1}')
        url = f"{base_url}proxy-list?page={i + 1}"
        soup = bs(get_page(url).content, "html.parser")
        proxies += parse_proxies(soup)

    logger.debug('get done')
    return proxies


list_proxies = get_free_proxies()
logger.info(f'find proxies - {len(list_proxies)}:')

__all__ = ['list_proxies']
