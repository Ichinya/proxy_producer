import requests

from utils import Logger

logger = Logger.get_logger(__name__)
logger.info('Get proxies from VPN GATE')

try:
    filecsv = requests.get('https://www.vpngate.net/api/iphone/').text
    vpn_data = filecsv.replace('\r', '')
    logger.info(f"Get {len(vpn_data)} proxies")
    servers = [line.split(',') for line in vpn_data.split('\n')]
except Exception as ex:
    logger.error(str(ex))
    servers = []

servers = [s for s in servers[2:] if len(s) > 1]
list_proxies = [f'socks5://vpn:vpn@{s[1]}:443' for s in servers]
logger.info(f'Result vpn {len(list_proxies)}')

__all__ = ['list_proxies']
