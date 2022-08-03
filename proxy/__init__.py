from proxy.free_proxy_list import list_proxies as free_proxy_list
from proxy.freeproxylistru import list_proxies as freeproxylistru
from proxy.jetkai import list_proxies as jetkai_proxy_list
from utils import Logger

logger = Logger.get_logger(__name__)
logger.info('Proxies get')

list_proxies = jetkai_proxy_list + free_proxy_list + freeproxylistru

__all__ = ["list_proxies"]
