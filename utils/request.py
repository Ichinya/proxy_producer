import os

import requests
from FakeAgent import Fake_Agent
from dotenv import load_dotenv

from utils import Logger

fa = Fake_Agent()

load_dotenv()
TIMEOUT = int(os.getenv('TIMEOUT') or 5)

logger = Logger.get_logger(__name__)


def headers():  # Socket headers send metod...
    return {
        "User-Agent": fa.random().strip(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }


def get_page(url):
    s = requests.Session()
    return s.get(url, timeout=TIMEOUT, headers=headers())


__all__ = ['get_page']
