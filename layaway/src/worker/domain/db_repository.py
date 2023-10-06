from abc import ABCMeta, abstractmethod

from shared.infrastructure.logs import Log


class DBRepository(metaclass=ABCMeta):

    @abstractmethod
    def is_alive(self, log: Log) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_error_details(self, log: Log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username: str, log: Log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user_data: dict, log: Log) -> dict:
        raise NotImplementedError
