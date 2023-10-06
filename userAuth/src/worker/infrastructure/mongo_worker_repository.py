import time

from shared.infrastructure import CachedConfig
from shared.infrastructure.logs import Log, Measurement
from shared.infrastructure.settings import get_settings
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository

settings = get_settings()


class MongoWorkerRepository(DBRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.document_error = "Without the document or it has a bad structure."

    def is_alive(self, log: Log) -> bool:
        init_time = time.perf_counter()

        with self.session_factory() as session:
            data: dict = session.is_alive()
            success = data.get('status')
            message = data.get('message')
            method_name = data.get('method')

            time_elapsed = Utils.get_time_elapsed_ms(init_time)

            if not success:
                measurement = Measurement('MongoDB', time_elapsed, 'Error')
                log.error("MongoDB is not alive", method_name,
                          message, None, measurement)
                return False

            measurement = Measurement('MongoDB', time_elapsed)
            log.info("MongoDB is alive", None, measurement)

            return True

    def check_db(self):
        with self.session_factory() as session:
            data = session.is_alive()
            return data.get('status')

    @CachedConfig()
    def get_error_details(self, log: Log, *args, **kwargs) -> dict | None:
        method_name = Utils.get_method_name(self, 'get_error_details')
        init_time = time.perf_counter()

        if not self.check_db():
            return

        with self.session_factory() as session:
            db = session.get_db(db_name=settings.MONGO_DB_NAME)
            collection = db.configs
            document_id = {'_id': settings.MONGO_ID_ERROR_DETAILS}
            results = collection.find_one(document_id)

            time_elapsed = Utils.get_time_elapsed_ms(init_time)

            if not results or not results.get('errors'):
                measurement = Measurement('MongoDB', time_elapsed, 'Error')
                log.error("Error: Get List of Error Details", method_name,
                          self.document_error, document_id, measurement)
                return {}

            measurement = Measurement('MongoDB', time_elapsed)
            log.info("Success: Get List of Error Details",
                     document_id, measurement)

            return results['errors']

    def get_user(self, username: str, log: Log) -> dict | None:
        init_time = time.perf_counter()

        if not self.check_db():
            return

        with self.session_factory() as session:
            db = session.get_db(db_name=settings.MONGO_DB_NAME_USERS)
            collection = db.users
            query = {'username': username}
            result = collection.find_one(query)

            time_elapsed = Utils.get_time_elapsed_ms(init_time)

            if not result:
                return {}

            measurement = Measurement('MongoDB', time_elapsed)
            log.info('Mongo: Get User', query, measurement)

            return result

    def create_user(self, user_data: dict, log: Log) -> bool | None:
        init_time = time.perf_counter()

        if not self.check_db():
            return

        with self.session_factory() as session:
            db = session.get_db(db_name=settings.MONGO_DB_NAME_USERS)
            collection = db.users
            collection.insert_one(user_data)

            time_elapsed = Utils.get_time_elapsed_ms(init_time)
            measurement = Measurement('MongoDB', time_elapsed)
            log.info('Mongo: Create user', None, measurement)

            return True
