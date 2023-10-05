from abc import ABCMeta, abstractmethod


class CacheRepository(metaclass=ABCMeta):

    @abstractmethod
    def is_alive(self, log) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, key, log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, key, data, log) -> None:
        raise NotImplementedError
