from db_api import db
from proxy import list_proxies


def update():
    db.add_proxies(list_proxies)


if __name__ == '__main__':
    update()
