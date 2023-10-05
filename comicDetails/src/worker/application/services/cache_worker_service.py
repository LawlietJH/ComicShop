from worker.domain import CacheRepository


class CacheWorkerService(CacheRepository):

    def __init__(self, cache_worker_repository: CacheRepository) -> None:
        self.__cache_repository = cache_worker_repository
        self.log = None

    def is_alive(self, **kwargs) -> bool:
        return self.__cache_repository.is_alive(self.log, **kwargs)

    def get_value(self, key: str, **kwargs) -> dict:
        return self.__cache_repository.get_value(key, self.log, **kwargs)

    def set_value(self, key: str, data: dict, **kwargs) -> dict:
        return self.__cache_repository.set_value(key, data, self.log, **kwargs)
