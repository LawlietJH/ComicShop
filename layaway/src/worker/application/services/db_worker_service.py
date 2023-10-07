from worker.domain import DBRepository


class DBWorkerService(DBRepository):
    def __init__(self, db_worker_repository: DBRepository) -> None:
        self.__db_repository = db_worker_repository
        self.log = None

    def is_alive(self, **kwargs) -> bool:
        return self.__db_repository.is_alive(self.log, **kwargs)

    def get_error_details(self, **kwargs) -> dict:
        return self.__db_repository.get_error_details(self.log, **kwargs)

    def get_layaway(self, user_id: int, **kwargs) -> dict:
        return self.__db_repository.get_layaway(user_id, self.log, **kwargs)

    def create_layaway(self, user_data: dict, **kwargs) -> dict:
        return self.__db_repository.create_layaway(user_data, self.log, **kwargs)

    def update_layaway(self, user_id: int, comic: dict, **kwargs) -> dict:
        return self.__db_repository.update_layaway(user_id, comic, self.log, **kwargs)
