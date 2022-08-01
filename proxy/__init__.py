from utils import Logger

# from proxy.vpn_gate import list_proxies as vpn_list
from proxy.jetkai import list_proxies as jetkai_proxy_list
from proxy.free_proxy_list import list_proxies as free_proxy_list

logger = Logger.get_logger(__name__)
logger.info('Proxies get')

list_proxies = jetkai_proxy_list + free_proxy_list

__all__ = ["list_proxies"]
