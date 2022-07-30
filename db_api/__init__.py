from db_api.mysql import DB
from dotenv import load_dotenv

load_dotenv()

db = DB()
db.connect()

__all__ = ['db']
