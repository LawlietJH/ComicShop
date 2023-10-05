import time

from firebase_admin import db

from shared.infrastructure.logs import Log, Measurement
from shared.infrastructure.settings import get_settings
from shared.infrastructure.utils import Utils
from worker.domain import RealTimeDBRepository

settings = get_settings()


class FirebaseRealTimeWorkerRepository(RealTimeDBRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def is_alive(self, log: Log) -> bool:
        with self.session_factory() as session:
            init_time = time.perf_counter()

            data: dict = session.is_alive()
            success = data.get('status')
            message = data.get('message')
            method_name = data.get('method')

            time_elapsed = Utils.get_time_elapsed_ms(init_time)

            if success:
                measurement = Measurement('MongoDB', time_elapsed)
                log.info("Firebase Real Time is alive",
                         measurement=measurement)
            else:
                measurement = Measurement('MongoDB', time_elapsed, 'Error')
                log.error("Firebase Real Time is not alive",
                          method=method_name, error=message,
                          measurement=measurement)

            return success

    def get_data(self, db_url: str, path: str, log: Log):
        init_time = time.perf_counter()
        with self.session_factory() as session:
            app = session.get_app(db_url)
            reference = db.reference(path, app)
            query_result = reference.get()

            time_elapsed = Utils.get_time_elapsed_ms(init_time)
            measurement = Measurement(f"Firebase: {db_url}{path}.json", time_elapsed)
            log.info(f"Getting {path} from firebase", measurement=measurement)

            return query_result
