from abc import ABCMeta, abstractmethod


class RealTimeDBRepository(metaclass=ABCMeta):

    @abstractmethod
    def is_alive(self, log) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_data(self, db_name: str, path: str, log) -> dict:
        raise NotImplementedError
