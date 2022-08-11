import os
from datetime import date, timedelta

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.elements import or_, and_
from sqlalchemy.sql.functions import now

from db_api.models import *
from utils import Logger

logger = Logger.get_logger(__name__)

load_dotenv()

DB_HOST = str(os.environ.get('DB_HOST') or os.getenv('DB_HOST') or 'localhost')
DB_NAME = str(os.environ.get('DB_NAME') or os.getenv('DB_NAME') or 'homestead')
DB_PORT = str(os.environ.get('DB_PORT') or os.getenv('DB_PORT') or '5531')
DB_USER = str(os.environ.get('DB_USER') or os.getenv('DB_USER') or 'root')
DB_PASS = str(os.environ.get('DB_PASS') or os.getenv('DB_PASS') or '')

POSTGRES_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Database:
    engine: AsyncEngine
    session: Session

    def __init__(self):
        logger.debug('DB Init')
        try:
            self.create_connect()
            self.create_all()
        except Exception as ex:
            logger.error(ex)

    def create_connect(self):
        logger.debug('DB create connect')
        self.engine = create_engine(POSTGRES_URI, echo=False)
        self.engine.connect()
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()

    def create_all(self):
        logger.debug('DB create tables')
        mapper_registry.metadata.create_all(self.engine)
        self.session.commit()

    def get_check_proxies(self):
        return self.session.query(Proxy).filter(
            and_(
                Proxy.send_to_mq.is_(None),
                or_(
                    Proxy.check_at < date.today() - timedelta(hours=3),
                    Proxy.check_at.is_(None)
                )
            )
        ).all()

    def check_old_proxies(self):
        self.session.query(Proxy).filter(
            or_(
                Proxy.check_at < date.today() - timedelta(hours=24),
                and_(
                    Proxy.send_to_mq < date.today() - timedelta(hours=24),
                    Proxy.check_at.is_(None)
                )
            )
        ).update({Proxy.check_at: None, Proxy.send_to_mq: None})
        self.session.commit()

    def proxy_send_to_mq(self, id_proxy):
        self.session.query(Proxy).filter(Proxy.id == id_proxy).update({Proxy.send_to_mq: now()})
        self.session.commit()

    def save_checked_proxy(self, id_proxy, params):
        self.session.query(Proxy).filter(Proxy.id == id_proxy).update(params)
        self.session.commit()

    def add_proxies(self, proxies):
        logger.info(f'Add proxies {len(proxies)}')
        for proxy in proxies:
            db_proxy = self.session.query(Proxy).filter(Proxy.proxy == proxy.get('proxy')).first()
            if db_proxy:
                continue
            db_proxy = Proxy(**proxy)
            self.session.add(db_proxy)
        self.session.commit()

    def __del__(self):
        logger.info('DEL')
        self.session.close_all()
        self.engine.dispose()


__all__ = ['Database']
