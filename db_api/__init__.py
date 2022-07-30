from db_api.mysql import DB
from utils import Logger

db = DB()
db.connect()

__all__ = ['db']
