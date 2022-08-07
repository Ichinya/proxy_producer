from bs4 import BeautifulSoup as bs
from sqlalchemy.sql.functions import now

from utils import Logger, get_page

logger = Logger.get_logger(__name__)


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    logger.debug('get proxy from free-proxy-list.net')
    # получаем ответ HTTP и создаем объект soup
    soup = bs(get_page(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append({'proxy': host, 'import_at': now()})
        except IndexError:
            continue
    logger.debug('get done')
    return proxies


list_proxies = get_free_proxies()
logger.info(f'Обнаружено бесплатных прокси - {len(list_proxies)}:')

__all__ = ['list_proxies']
