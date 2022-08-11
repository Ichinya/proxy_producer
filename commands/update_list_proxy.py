from db_api import db
from proxy import proxies_to_db


def update_list_proxy():
    proxies_to_db(db)


__all__ = ['update_list_proxy']
