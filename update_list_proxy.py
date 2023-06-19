from tendo import singleton
from tendo.singleton import SingleInstanceException

from commands.update_list_proxy import update_list_proxy

if __name__ == '__main__':
    try:
        me = singleton.SingleInstance()
    except SingleInstanceException as ex:
        exit('Скрипт уже запущен')
    update_list_proxy()
