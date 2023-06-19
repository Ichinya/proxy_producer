from tendo import singleton
from tendo.singleton import SingleInstanceException

from commands.send_to_mq import send_to_mq

if __name__ == '__main__':
    try:
        me = singleton.SingleInstance()
    except SingleInstanceException as ex:
        exit('Скрипт уже запущен')
    send_to_mq()
