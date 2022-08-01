import os

import mysql.connector
from mysql.connector import errorcode

from db_api.tables import TABLES
from utils import Logger

DB_HOST = str(os.environ.get('DB_HOST') or os.getenv('DB_HOST') or 'localhost')
DB_NAME = str(os.environ.get('DB_NAME') or os.getenv('DB_NAME') or 'homestead')
DB_PORT = str(os.environ.get('DB_PORT') or os.getenv('DB_PORT') or '3306')
DB_USER = str(os.environ.get('DB_USER') or os.getenv('DB_USER') or 'root')
DB_PASS = str(os.environ.get('DB_PASS') or os.getenv('DB_PASS') or '')

logger = Logger.get_logger(__name__)


class DB:

    def __init__(self):
        logger.info('DB init')
        self.cnx = None
        self.cur = None

    def create_database(self):
        logger.info('create_database')
        try:
            self.cur.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            logger.critical("Failed creating database: {}".format(err))
            exit(1)

    def connect(self):
        logger.info('connect')
        # Connect to server
        self.cnx = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        # Get a cursor
        self.cur = self.cnx.cursor(dictionary=True)

        try:
            self.cur.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            logger.error("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                logger.info("Database {} created successfully.".format(DB_NAME))
                self.cnx.database = DB_NAME
            else:
                logger.critical(err)
                exit(1)
        self.create_table()

    def create_table(self):
        logger.info('create_table')
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                logger.info(f"Creating table: {table_name}")
                self.cur.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info("already exists.")
                else:
                    logger.error(err.msg)
            else:
                logger.info("OK")

    def get_check_proxies(self):
        query = '''
        SELECT * FROM proxies WHERE send_to_mq IS NULL AND is_vpn=0
        '''
        self.cur.execute(query)
        proxies = []
        for proxy in self.cur:
            proxies.append(proxy)
        return proxies

    def get_check_vpn(self):
        query = '''
         SELECT * FROM proxies WHERE send_to_mq IS NULL AND is_vpn=1
         '''
        self.cur.execute(query)
        proxies = []
        for proxy in self.cur:
            proxies.append(proxy)
        return proxies

    def check_old_proxies(self):
        query = "UPDATE proxies SET send_to_mq=NULL, check_at=NULL WHERE check_at < DATE_SUB(NOW(), INTERVAL 3 HOUR)"
        self.cur.execute(query)
        self.cnx.commit()

    def proxy_send_to_mq(self, id_proxy):
        query = "UPDATE proxies SET send_to_mq=NOW() WHERE id = %(id)s"
        self.cur.execute(query, {'id': id_proxy})
        emp_no = self.cur.lastrowid
        self.cnx.commit()
        return emp_no

    def save_checked_proxy(self, id_proxy, params):
        queue = "UPDATE proxies SET check_at=NOW(), is_good=%(is_good)s WHERE id = %(id)s"
        params["id"] = id_proxy
        self.cur.execute(queue, params)
        emp_no = self.cur.lastrowid
        self.cnx.commit()
        return emp_no

    def add_proxies(self, proxies):
        logger.info(f'Add proxies {len(proxies)}')
        sql = '''
        INSERT INTO proxies 
            (proxy, is_vpn, import_at) 
        VALUES(%(proxy)s, %(is_vpn)s, NOW()) 
        ON DUPLICATE KEY UPDATE
            import_at=NOW()
        '''
        for item in proxies:
            data_proxy = {'proxy': item.get('proxy'), 'is_vpn': item.get('is_vpn') or 0}
            self.cur.execute(sql, data_proxy)
        self.cnx.commit()

    def close(self):
        logger.info('CLOSE')
        self.cur.close()
        self.cnx.close()

    def __del__(self):
        logger.info('DEL')
        try:
            self.cur.close()
            self.cnx.close()
        except:
            pass


__all__ = ['DB']
