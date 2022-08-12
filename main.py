import json
import time

from sqlalchemy.sql.functions import now

from mq import mq
from utils import Logger

logger = Logger.get_logger(__name__)


def receive_msg(ch, method, properties, body):
    from db_api import db
    logger.info('received msg')
    proxy = json.loads(body.decode('utf8'))
    checked_proxy = {'is_good': proxy.get('is_good', 0), 'check_at': now(), 'send_to_mq': None}
    db.save_checked_proxy(proxy.get('id'), checked_proxy)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_checked_proxy():
    mq.connect_to_queue('checked_proxy')
    mq.channel.basic_qos(prefetch_count=1)
    mq.channel.basic_consume(queue='checked_proxy', on_message_callback=receive_msg)
    mq.channel.start_consuming()


if __name__ == '__main__':
    while True:
        try:
            update_checked_proxy()
        except Exception as ex:
            logger.error(str(ex))
            time.sleep(3)
