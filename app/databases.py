import os
import pickle
from typing import Any

import redis  # type: ignore
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Получение данных для подключения к БД
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
# Подключение к БД
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = Session()

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')


def get_redis_client():
    return redis.Redis(host=f'{REDIS_HOST}', port=REDIS_PORT, db=0)


class RedisCache:
    def __init__(self, redis_client: redis.Redis = get_redis_client()) -> None:
        self.client = redis_client
        self.time_to_live = 300

    def set_cache(self, key: Any, value: Any) -> bool:
        data = pickle.dumps(value)
        return self.client.setex(str(key), self.time_to_live, data)

    def clear_cache(self, address: str) -> None:
        for key in self.client.scan_iter(address):
            self.client.delete(key)

    def get_cache(self, key: Any) -> Any | None:
        data = self.client.get(str(key))
        if data is not None:
            return pickle.loads(data)
        return None

    def delete_cache(self, key: Any) -> int:
        return self.client.delete(str(key))

    def clear_all_cache(self, menu_id: int | str) -> None:
        self.clear_cache(f'{menu_id}*')
        self.clear_cache('all*')
