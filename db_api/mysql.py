import mysql.connector
from mysql.connector import errorcode

from db_api.tables import TABLES
from utils import Logger

DB_NAME = 'homestead'

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
            host="127.0.0.1",
            port=3306,
            user="user",
            password="pass",
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
        SELECT * FROM proxies WHERE send_to_mq IS NULL
        '''
        self.cur.execute(query)
        proxies = []
        for proxy in self.cur:
            proxies.append(proxy)
        return proxies

    def proxy_send_to_mq(self, id_proxy):
        query = "UPDATE proxies SET send_to_mq=NOW() WHERE id = %(id)s"
        self.cur.execute(query, {'id': id_proxy})
        emp_no = self.cur.lastrowid
        self.cnx.commit()
        return emp_no

    def add_proxies(self, proxies):
        logger.info(f'Add proxies {len(proxies)}')
        sql = '''
        INSERT INTO proxies 
            (proxy, import_at) 
        VALUES(%(proxy)s, NOW()) 
        ON DUPLICATE KEY UPDATE
            import_at=NOW()
        '''
        for proxy in proxies:
            data_proxy = {'proxy': proxy}
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
