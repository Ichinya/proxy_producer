import json

from db_api import db
from mq import mq


def send_to_mq():
    db.check_old_proxies()
    for proxy in db.get_check_proxies():
        mq.send_task(json.dumps(proxy, indent=4, sort_keys=True, default=str))
        db.proxy_send_to_mq(proxy.get('id'))

    # mq.connect_to_queue('check_vpn')
    # for proxy in db.get_check_vpn():
    #     mq.send_task(json.dumps(proxy, indent=4, sort_keys=True, default=str))
    #     db.proxy_send_to_mq(proxy.get('id'))


if __name__ == '__main__':
    send_to_mq()
