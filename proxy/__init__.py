from utils import Logger
from proxy.vpn_gate import list_proxies

logger = Logger.get_logger(__name__)
logger.info('Proxies get')


__all__ = ["list_proxies"]
