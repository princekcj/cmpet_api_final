import platform
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings
import os

mode = os.environ.get('DB_MODE')
db_host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
db_nme = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
pwd = os.environ.get('DB_PSWD')
api_keys = os.environ.get('VALID_API_KEYS')






def is_debug():
    system = platform.system()
    dev_system = ('Windows', 'Darwin')
    return True if system in dev_system else False


class Settings(BaseSettings):
    # mode
    DEBUG: bool = is_debug()

    PROJECT: ClassVar[str] = ''

    # db
    DB_MODE: ClassVar[str] = mode
    DB_HOST: ClassVar[str] = db_host
    DB_PORT: ClassVar[int] = port  # Add the port number here
    DB_NAME: ClassVar[str] = db_nme
    DB_USER: ClassVar[str] = db_user
    DB_PSWD: ClassVar[str] = pwd

    # redis  hy
    REDIS_HOST: ClassVar[str] = '' if not DEBUG else 'localhost'
    REDIS_DB: ClassVar[int] = 1

    # time
    utc: ClassVar[str] = 'UTC'
    timezone: ClassVar[str] = 'Europe/London'
    format: ClassVar[str] = 'YYYY-MM-DD HH:mm:ss'


data_settings = Settings()
