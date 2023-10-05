import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer

from shared.domain.response import Response, SuccessResponse
from shared.infrastructure import ErrorResponse, Settings, Utils
from shared.infrastructure.logs import Log
from worker.domain import DBRepository


class UpdateCacheUseCase:

    def __init__(self, db_worker_service: DBRepository, log: Log,
                 settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self.settings = settings
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()
        self.db_general_config = None
        self.db_service_config = None
        self.db_error_details = None

    @autodynatrace.trace('UpdateCacheUseCase - execute')
    @tracer.wrap(service='basetemplate', resource='execute')
    def execute(self) -> Response:
        self._set_logs()

        self._log.info('Start: Update Config')

        self.db_general_config = self.__db_service.get_general_config(update_cache=True)
        self.db_service_config = self.__db_service.get_service_config(update_cache=True)
        self.db_error_details = self.__db_service.get_error_details(update_cache=True)

        if not self.db_general_config or not self.db_service_config \
                or not self.db_error_details:
            raise ErrorResponse(
                error_code=100,
                message="Error de conexión a mongo.",
                code_name='500.General-Error.100',
                transaction_id=self.transaction_id,
                status_code=500)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info('Update cache config: Success')
        data = {'status': "Successful"}
        return SuccessResponse(
            data=data, status_code=200, transaction_id=self.transaction_id,
            time_elapsed=total_time_elapsed)

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
