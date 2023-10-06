import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer
from shared.domain.response import FailureResponse, Response, SuccessResponse
from shared.infrastructure import Settings, Utils
from shared.infrastructure.logs import Log, Measurement
from worker.domain import DBRepository


class ReadinessUseCase:
    def __init__(self, db_worker_service: DBRepository, log: Log,
                 settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self.settings = settings
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('ReadinessUseCase - execute')
    @tracer.wrap(service='userauth', resource='execute')
    def execute(self) -> Response:
        self._set_logs()

        self._log.info("Start: /readiness")

        if not self.__db_service.is_alive():
            time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
            self._log.error(
                "Error al obtener configuraciones de MongoDB.",
                method=Utils.get_method_name(self, 'execute'),
                error="Ha ocurrido un error al obtener las configuraciones",
                measurement=Measurement('MongoDB', time_elapsed, 'Error'))
            return FailureResponse(
                {'user_message': "Error de conexión a mongo"}, 500,
                self.transaction_id, error_code=100)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)

        self._log.info("Mongo is alive")

        return SuccessResponse({'status': "Mongo is alive"}, 200,
                               self.transaction_id, total_time_elapsed)

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
