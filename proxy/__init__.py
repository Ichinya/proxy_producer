from utils import Logger

logger = Logger.get_logger(__name__)


def proxies_to_db(db):
    logger.info('Proxies get')
    from proxy.raw_list import proxies_to_db
    proxies_to_db(db)
    from proxy.free_proxy_list import list_proxies
    db.add_proxies(list_proxies)
    from proxy.freeproxylistru import list_proxies
    db.add_proxies(list_proxies)
    from proxy.jetkai import list_proxies
    db.add_proxies(list_proxies)


__all__ = ["proxies_to_db"]
