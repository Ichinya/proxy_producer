import json

from db_api import db
from mq import mq
from utils import Logger

logger = Logger.get_logger(__name__)


def receive_msg(ch, method, properties, body):
    logger.info('received msg')
    proxy = json.loads(body.decode('utf8'))
    proxy['is_good'] = proxy.get('is_good', 0)
    db.save_checked_proxy(proxy.get('id'), proxy)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_checked_proxy():
    mq.connect_to_queue('checked_proxy')
    mq.channel.basic_qos(prefetch_count=1)
    mq.channel.basic_consume(queue='checked_proxy', on_message_callback=receive_msg)
    mq.channel.start_consuming()


if __name__ == '__main__':
    update_checked_proxy()
