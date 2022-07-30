import logging
import os

from dotenv import load_dotenv

# Грузим и устанавливаем первоначальные настройки
load_dotenv()

# Параметры логгера
LOG_LEVEL_OUT = int(os.getenv('LOG_LEVEL_OUT') or logging.INFO)
LOG_LEVEL_FILE = int(os.getenv('LOG_LEVEL_FILE') or logging.WARNING)
LOG_FILE = str(os.getenv('LOG_FILE') or 'log_warning.log')

_log_format = "%(asctime)s [%(levelname)s] %(name)s - (%(filename)s).%(funcName)s(%(lineno)d): %(message)s"


class Logger:
    @staticmethod
    def get_file_handler():
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(LOG_LEVEL_FILE)
        file_handler.setFormatter(logging.Formatter(_log_format))
        return file_handler

    @staticmethod
    def get_stream_handler():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LOG_LEVEL_OUT)
        stream_handler.setFormatter(logging.Formatter(_log_format))
        return stream_handler

    @staticmethod
    def get_logger(name):
        log_adapter = logging.getLogger(name)
        log_adapter.setLevel(LOG_LEVEL_OUT)
        log_adapter.addHandler(Logger.get_file_handler())
        log_adapter.addHandler(Logger.get_stream_handler())
        return log_adapter


__all__ = [Logger]
