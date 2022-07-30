import logging

import pika


class MQ:

    def __init__(self, logger: logging, url: str):
        self.queue = None
        self.logger = logger
        url_params = pika.URLParameters(url)
        # connect to rabbitmq
        self.connection = pika.BlockingConnection(url_params)
        self.channel = self.connection.channel()
        self.logger.debug('class MQ created')
        # self.clear_queue()

    def clear_queue(self):
        self.logger.debug('clear_queues')
        self.channel.queue_purge(queue='check_proxy')
        self.channel.queue_delete(queue='check_proxy')

    def connect_to_queue(self, queue):
        self.logger.debug(f'connect to {queue}')
        self.queue = queue
        # declare a new queue
        # durable flag is set so that messages are retained
        # in the rabbitmq volume even between restarts
        self.channel.queue_declare(queue=queue, durable=True)
        self.logger.info('Queue start')

    def send_task(self, body):
        self.logger.debug(f'send_task {str(self.queue)}')
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        self.logger.debug("Produced the message")

    def __del__(self):
        self.logger.debug('DEL MQ')
        # close the channel and connection
        # to avoid program from entering with any lingering
        # message in the queue cache
        self.channel.close()
        self.connection.close()


__all__ = ['MQ']
