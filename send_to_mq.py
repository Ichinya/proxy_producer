import json

from db_api import db
from mq import mq


def send_to_mq():
    db.check_old_proxies()
    for proxy in db.get_check_proxies():
        mq.send_task(json.dumps(proxy.to_dict(), indent=4, sort_keys=True, default=str))
        db.proxy_send_to_mq(proxy.__getattribute__('id'))


if __name__ == '__main__':
    send_to_mq()
