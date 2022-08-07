from urllib.request import Request, urlopen
import re

from sqlalchemy.sql.functions import now

from utils import Logger
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

raw_lists_proxies = [
    'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http',
    'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks',
    'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks',
    'http://worm.rip/http.txt',
    'http://worm.rip/socks4.txt',
    'http://worm.rip/socks5.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5',
    'https://openproxy.space/list/http',
    'https://openproxy.space/list/socks4',
    'https://openproxy.space/list/socks5',
    'https://openproxylist.xyz/http.txt',
    'https://openproxylist.xyz/socks4.txt',
    'https://openproxylist.xyz/socks5.txt',
    'https://proxyspace.pro/http.txt',
    'https://proxyspace.pro/https.txt',
    'https://proxyspace.pro/socks4.txt',
    'https://proxyspace.pro/socks5.txt',
    'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt',
    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt',
    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
    'https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt',
    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
    'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
    'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt',
    'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt',
    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt',
    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://rootjazz.com/proxies/proxies.txt',
    'https://sheesh.rip/http.txt',
    'https://spys.me/proxy.txt',
    'https://www.freeproxychecker.com/result/http_proxies.txt',
    'https://www.freeproxychecker.com/result/socks4_proxies.txt',
    'https://www.freeproxychecker.com/result/socks5_proxies.txt',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxy-list.download/api/v1/get?type=https',
    'https://www.proxy-list.download/api/v1/get?type=socks4',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://www.proxyscan.io/download?type=http',
    'https://www.proxyscan.io/download?type=socks4',
    'https://www.proxyscan.io/download?type=socks5',
]

logger = Logger.get_logger(__name__)


def get_proxies(sources, is_url=False):
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
    data = ""
    for source in sources:
        logger.debug(f'get proxies from {source}')
        try:
            if is_url:
                req = Request(source, headers={'User-Agent': ua.random})
                response = urlopen(req)
                data += response.read().decode('utf-8') + "\n"
            else:
                with open(source) as file:
                    data += file.read() + "\n"
            logger.debug("Processed: " + source)
        except Exception:
            logger.error("Skipping, Error Occured: " + source)
    return re.findall(pattern, data)


logger.info('Begin downloads list proxies')
proxies = get_proxies(raw_lists_proxies, is_url=True)
list_proxies = list(map(lambda item: {'proxy': item, 'import_at': now()}, proxies))
logger.info(f'Обнаружено прокси - {len(list_proxies)}:')

__all__ = ['list_proxies']
