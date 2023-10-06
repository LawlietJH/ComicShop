import asyncio
import copy
import json
import time
import uuid

import autodynatrace
from ddtrace import tracer
from jose import ExpiredSignatureError, JWSError
from passlib.context import CryptContext
from passlib.hash import des_crypt, md5_crypt, sha256_crypt
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse, Settings
from shared.infrastructure.logs import Log, Measurement
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository
from worker.domain.entities import UserRegistration
from worker.domain.schemas import SecuritySchema

from .functionalities import Functionalities

crypt_context = CryptContext([sha256_crypt, md5_crypt, des_crypt])


class ValidateTokenUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._security_schema = SecuritySchema()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('ValidateTokenUseCase - execute')
    @tracer.wrap(service='userauth', resource='execute')
    def execute(self, token: str) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        object_ = {'token': token}
        self._log.info("Start: /keys", object_)

        data = self._get_data(token)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("Get User Successfully")

        data = {'user': data}
        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _get_data(self, token: str):
        method_name = Utils.get_method_name(self, '_get_response')
        init_time = time.perf_counter()
        measurement = Measurement('JWT', 0, 'Error')
        error_104 = ErrorResponse(**self._error_attributes(104))

        try:
            decoded_token = self._security_schema.decode_access_token(token)
            user = json.loads(decoded_token)['sub']
            if not user:
                measurement.time_elapsed = Utils.get_time_elapsed_ms(init_time)
                self._log.error("Without payload", method_name,
                                "User does not exist", None, measurement)
                raise error_104

            user.pop('password')
            return user

        except JWSError as error:
            measurement.time_elapsed = Utils.get_time_elapsed_ms(init_time)
            self._log.error("Invalid token", method_name,
                            error, None, measurement)
            error_104.meta['details'] = "Invalid token or incorrect secret key"
        except ExpiredSignatureError as error:
            measurement.time_elapsed = Utils.get_time_elapsed_ms(init_time)
            self._log.error("Expired token", method_name,
                            error, None, measurement)
            error_104.meta['details'] = "Token has expired"
        except Exception as error:
            measurement.time_elapsed = Utils.get_time_elapsed_ms(init_time)
            self._log.error("General error", method_name,
                            error, None, measurement)
            error_104.meta['details'] = "Could not decode the token"

        raise error_104

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
