from abc import ABCMeta, abstractmethod

from shared.infrastructure.logs import Log


class DBRepository(metaclass=ABCMeta):

    @abstractmethod
    def is_alive(self, log: Log) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_error_details(self, log: Log) -> dict:
        raise NotImplementedError
