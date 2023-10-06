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
from worker.domain.entities import UserRegistration
from worker.domain.schemas import SecuritySchema

from .functionalities import Functionalities

crypt_context = CryptContext([sha256_crypt, md5_crypt, des_crypt])


class LoginUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._security_schema = SecuritySchema()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('GetRecordUseCase - execute')
    @tracer.wrap(service='userauth', resource='execute')
    def execute(self, user: UserRegistration) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        object_ = user.dict(exclude={'password'})
        self._log.info("Start: /singup", object_)

        token = self._get_data(user)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("User Created Successfully")

        data = {'token': token}
        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _get_data(self, user: UserRegistration):
        method_name = Utils.get_method_name(self, '_set_data')
        init_time = time.perf_counter()

        existing_user = self.__db_service.get_user(user.username)
        total_time_elapsed = Utils.get_time_elapsed_ms(init_time)

        if existing_user is None:
            measurement = Measurement('MongoDB', total_time_elapsed, 'Error')
            self._log.error("Failed to Get User", method_name,
                            "Mongo is not up", None, measurement)
            raise ErrorResponse(**self._error_attributes(100))

        elif not existing_user:
            error_message = "User Does Not Exist"
            measurement = Measurement('/signup', total_time_elapsed, 'Error')
            self._log.error("Failed to Get User", method_name,
                            error_message, None, measurement)
            raise ErrorResponse(**self._error_attributes(107),
                                details="User does not exist")

        hashed_password = existing_user.get('password')
        if not crypt_context.verify(user.password, hashed_password):
            error_message = "Invalid Password"
            measurement = Measurement('MongoDB', total_time_elapsed, 'Error')
            self._log.error(error_message, method_name,
                            "Password is incorrect", None, measurement)
            raise ErrorResponse(None, error_message)

        existing_user.pop('_id')
        token = self._security_schema.create_access_token(existing_user)

        return token

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
