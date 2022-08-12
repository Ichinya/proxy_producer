import json

from db_api import db
from mq import mq


def send_to_mq():
    db.check_old_proxies()
    for proxy in db.get_check_proxies():
        need_check_proxy = {'id': proxy.__getattribute__('id'), 'proxy': proxy.__getattribute__('proxy')}
        mq.send_task(json.dumps(need_check_proxy, indent=4, sort_keys=True, default=str))
        db.proxy_send_to_mq(proxy.__getattribute__('id'))


__all__ = ['send_to_mq']
