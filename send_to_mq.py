import json

from db_api import db
from mq import mq


def main():
    for proxy in db.get_check_proxies():
        mq.send_task(json.dumps(proxy, indent=4, sort_keys=True, default=str))
        db.proxy_send_to_mq(proxy.get('id'))


if __name__ == '__main__':
    main()
