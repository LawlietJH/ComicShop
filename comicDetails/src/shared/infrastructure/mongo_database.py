from collections.abc import Iterator
from contextlib import contextmanager, suppress

from pymongo import MongoClient
from shared.domain.database import Database, Session

from .settings import get_settings
from .utils import Utils

settings = get_settings()


class MongoSession(Session):
    def __init__(self, db_uri: str, app_name: str, max_pool_size: int, timeout: int) -> None:
        self.mongo_uri = db_uri
        self.__client = MongoClient(
            self.mongo_uri, maxPoolSize=max_pool_size,
            serverSelectionTimeoutMS=timeout, appName=app_name)

    def __enter__(self):
        return self

    def get_db(self, db_name: str) -> Database:
        return self.__client[db_name]

    def is_alive(self) -> dict:
        data = {
            'status': True,
            'message': 'Success',
            'method': Utils.get_method_name(self, 'is_alive')
        }

        try:
            self.__client.server_info()
            self.__client.admin.command('ping')
            collection = self.__client[settings.MONGO_DB_NAME].configuraciones
            collection.find_one({'_id': 'general'})
        except Exception as ex:
            data['status'] = False
            data['message'] = str(ex)

        return data

    def __exit__(self, exception_type, exception_value, traceback):
        self.__client.close()


class MongoDatabase(Database):
    def __init__(self, db_uri: str, app_name: str, max_pool_size: int, timeout: int) -> None:
        self.__session = MongoSession(
            db_uri, app_name, max_pool_size, timeout)

    @contextmanager
    def session(self) -> Iterator[Session]:
        """ Function used to obtain Mongo sessions """
        with suppress(Exception):
            yield self.__session
