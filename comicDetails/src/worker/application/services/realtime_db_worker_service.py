from worker.domain import RealTimeDBRepository


class RealTimeDBWorkerService(RealTimeDBRepository):

    def __init__(self,
                 realtime_db_worker_repository: RealTimeDBRepository) -> None:
        self.__realtime_db_repository = realtime_db_worker_repository
        self.log = None

    def is_alive(self) -> bool:
        return self.__realtime_db_repository.is_alive(self.log)

    def get_data(self, db_url: str, path: str) -> dict:
        return self.__realtime_db_repository.get_data(db_url, path, self.log)
