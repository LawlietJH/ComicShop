from abc import ABCMeta, abstractmethod


class DBRepository(metaclass=ABCMeta):

    @abstractmethod
    def is_alive(self, log) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_general_config(self, log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_service_config(self, log) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_error_details(self, log) -> dict:
        raise NotImplementedError
