import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer

from shared.domain import Response, SuccessResponse
from shared.infrastructure import (EndpointParams, ErrorResponse,
                                   GeneralRequestServer, Settings)
from shared.infrastructure.logs import Log
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository


class HelloWorldUseCase:

    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._general_request = GeneralRequestServer()
        self._endpoint_params = EndpointParams()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('HelloWorldUseCase - execute')
    @tracer.wrap(service='basetemplate', resource='execute')
    def execute(self, env: str = '') -> Response:
        # TODO: When working with them, we can make use of their 'measurement'
        #  attribute to add traceability to our transaction, in the readiness
        #  use case there is an example implementation and in the readme
        #  file you can find more information.
        self._set_logs()
        self._set_configs()

        self._log.info("Start: /service_name")

        self._endpoint_params.set_params(self.db_general_config, env)
        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)

        self._log.info("Hello World")

        return SuccessResponse(
            data={'status': "Hello World"},
            status_code=200,
            transaction_id=self.transaction_id,
            time_elapsed=total_time_elapsed
        )

    def _set_configs(self):
        self.db_general_config = self.__db_service.get_general_config()
        self.db_service_config = self.__db_service.get_service_config()
        self.db_error_details = self.__db_service.get_error_details()

        if not self.db_general_config or not self.db_service_config \
                or not self.db_error_details:
            raise ErrorResponse(
                error_code=100,
                message="Error de conexión a mongo.",
                code_name='500.General-Error.100',
                transaction_id=self.transaction_id,
                status_code=500)

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self._general_request.log = self._log_external
