import asyncio
import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer
from passlib.context import CryptContext
from passlib.hash import des_crypt, md5_crypt, sha256_crypt
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse, Settings
from shared.infrastructure.logs import Log, Measurement
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository
from worker.domain.entities import Layaway

from .functionalities import Functionalities


class SetLayawayUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('SetLayawayUseCase - execute')
    @tracer.wrap(service='layaway', resource='execute')
    def execute(self, body: Layaway) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        self._log.info("Start: POST /layaway", body.dict())

        self._set_data(body)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("Comic Added Successfully")

        data = {'message': f"The Comic '{body.id}' has been added successfully."}
        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _set_data(self, body: Layaway):
        pass

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
