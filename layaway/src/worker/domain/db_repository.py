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
    def get_layaway(self, user_id: int, log: Log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_layaway(self, user_data: dict, log: Log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_layaway(self, user_id: int, comic: dict, log: Log) -> dict:
        raise NotImplementedError
