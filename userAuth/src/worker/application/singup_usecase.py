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

from .functionalities import Functionalities

crypt_context = CryptContext([sha256_crypt, md5_crypt, des_crypt])


class SingupUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('SingupUseCase - execute')
    @tracer.wrap(service='userauth', resource='execute')
    def execute(self, user: UserRegistration) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        user.id = user.id.hex
        object_ = user.dict(exclude={'password'})
        self._log.info("Start: /singup", object_)

        self._set_data(user)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("User Created Successfully")

        data = {'message': f"The User '{user.username}' has been created successfully."}
        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _set_data(self, user: UserRegistration):
        method_name = Utils.get_method_name(self, '_set_data')
        init_time = time.perf_counter()

        existing_user = self.__db_service.get_user(user.username)
        total_time_elapsed = Utils.get_time_elapsed_ms(init_time)

        if existing_user is None:
            measurement = Measurement('MongoDB', total_time_elapsed, 'Error')
            self._log.error("Failed to Get User", method_name,
                            "Mongo is not up", None, measurement)
            raise ErrorResponse(**self._error_attributes(100))

        elif existing_user:
            error_message = "User Already Exist"
            measurement = Measurement('/signup', total_time_elapsed, 'Error')
            self._log.error("Failed to Create User", method_name,
                            error_message, None, measurement)
            raise ErrorResponse(None, error_message, self.transaction_id, 409)

        user.password = crypt_context.hash(user.password)
        user_data = user.dict()
        user_data['_id'] = user_data.pop('id')
        was_inserted = self.__db_service.create_user(user_data)

        if was_inserted is None:
            measurement = Measurement('MongoDB', total_time_elapsed, 'Error')
            self._log.error("Error Adding User", method_name,
                            "Mongo is not up", None, measurement)
            raise ErrorResponse(**self._error_attributes(100))

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
