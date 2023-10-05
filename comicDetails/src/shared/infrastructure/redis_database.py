from collections.abc import Iterator
from contextlib import contextmanager, suppress

from redis import Redis

from shared.domain.database import Database, Session

from .utils import Utils


class RedisSession(Session):
    """
    Class used to manage the Redis connection sessions.

    Parameters:
        redis_uri: redis database connection string

    Attributes:
        redis_uri: redis connection string
        __client: client with redis connection
    """

    def __init__(self, redis_uri: str) -> None:
        self.redis_uri = redis_uri
        self.__client = Redis(self.redis_uri)

    def __enter__(self):
        return self

    def get_connection(self) -> Redis:
        """ Gets the redis connection """
        return self.__client

    def is_alive(self) -> dict:
        """
        Function that verifies that the database connection is active.

        Return:
            Dictionary with connection status
        """
        data = {
            'status': True,
            'message': 'Success',
            'method': Utils.get_method_name(self, 'is_alive')
        }

        try:
            self.__client.ping()
        except Exception as ex:
            data['status'] = False
            data['message'] = str(ex)

        return data

    def __exit__(self, exception_type, exception_value, traceback):
        self.__client.client_kill(self.redis_uri)


class RedisDatabase(Database):
    """
    Class used to manage the Redis connection databases.

    Parameters:
        redis_uri: database connection string

    Attributes:
        __session: object with the connected Redis Session
    """

    def __init__(self, redis_uri: str) -> None:
        self.__session = RedisSession(redis_uri)

    @contextmanager
    def session(self) -> Iterator[Session]:
        with suppress(Exception):
            yield self.__session
