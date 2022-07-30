import os

from dotenv import load_dotenv

from mq.mq import MQ
from utils import Logger

logger = Logger.get_logger(__name__)

logger.info('Start MQ')
# Грузим и устанавливаем первоначальные настройки
load_dotenv()

# Очереди
AMQP_URL = str(
    os.environ['AMQP_URL'] or
    os.getenv('AMQP_URL') or
    'amqp://localhost?connection_attempts=10&retry_delay=9'
)

mq = MQ(logger=logger, url=AMQP_URL)
mq.connect_to_queue('check_proxy')

__all__ = ['mq', 'AMQP_URL']
