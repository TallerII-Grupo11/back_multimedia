from functools import lru_cache

from app.conf.config import Settings
from app.conf.mongodb import MongoDB


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_mongodb():
    return MongoDB()
