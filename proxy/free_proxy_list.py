import requests
from bs4 import BeautifulSoup as bs
from utils import Logger

logger = Logger.get_logger(__name__)


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    logger.info('get proxy from free-proxy-list.net')
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append({'proxy': host})
        except IndexError:
            continue
    logger.info('get done')
    return proxies


list_proxies = get_free_proxies()
logger.info(f'Обнаружено бесплатных прокси - {len(list_proxies)}:')

__all__ = ['list_proxies']
