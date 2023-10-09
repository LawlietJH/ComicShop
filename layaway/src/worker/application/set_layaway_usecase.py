import asyncio
import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse, GeneralRequestServer, Settings
from shared.infrastructure.logs import Log
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository
from worker.domain.entities import Comic, Layaway, User

from .functionalities import Functionalities


class SetLayawayUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._general_request = GeneralRequestServer()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('SetLayawayUseCase - execute')
    @tracer.wrap(service='layaway', resource='execute')
    def execute(self, token: str, body: Layaway) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        self._log.info("Start: POST /layaway", body.dict())

        self._set_data(token, body)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("Comic Added Successfully")

        data = {'message': f"The Comic '{body.comic_id}' has been added successfully."}
        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _set_data(self, token: str, body: Layaway):
        user = self._get_user(token)
        comic = self._get_comic_data(body.comic_id)
        user_data = self.__db_service.get_layaway(user_id=user.id)

        if not user_data:
            user_data = {
                '_id': user.id,
                'username': user.username,
                'layaway': []
            }
            success = self.__db_service.create_layaway(user_data)
            if not success:
                raise ErrorResponse(None, "Layaway was not created",
                                    self.transaction_id, 500)

        if comic.dict() in user_data['layaway']:
            raise ErrorResponse(None, f"The comic '{body.comic_id}' already exists in layaway",
                                self.transaction_id, 409)

        success = self.__db_service.update_layaway(user.id, comic.dict())
        if not success:
            raise ErrorResponse(None, f"The comic '{body.comic_id}' was not added to the layaway",
                                self.transaction_id, 500)

    # General Request ----------------------------------------------------------

    @autodynatrace.trace('SetLayawayUseCase - _get_user')
    @tracer.wrap(service='layaway', resource='_get_user')
    def _get_user(self, token: str) -> User:
        """ Obtiene un Usuario. """
        URL = f"{self._settings.URL_VALIDATE_TOKEN}"
        headers = {'Authorization': f"Bearer {token}"}
        coroutine = self._general_request.get(URL, headers=headers)
        response = asyncio.run(coroutine)

        if not response['response']:
            if response['type_error'] == 'timeout':
                raise ErrorResponse(**self._error_attributes(103))
            raise ErrorResponse(**self._error_attributes(102))

        adds: dict = response['additionals']

        if not response['success']:
            data = response['response']['data']
            meta = response['response']['meta']
            status = response['status']
            message = data.get('user_message', '')
            details = meta.get('details', None)
            self._request_log_error(adds['url'], message, adds['time_elapsed'],
                                    adds['reason'], 'GET')
            raise ErrorResponse(None, message, self.transaction_id, status,
                                details=details)

        self._request_log_info(adds['url'], "Success getting user data.",
                               adds['time_elapsed'], 'GET')

        user = User.parse_obj(response['response']['data']['user'])
        return user

    @autodynatrace.trace('SetLayawayUseCase - _get_comic_data')
    @tracer.wrap(service='layaway', resource='_get_comic_data')
    def _get_comic_data(self, comic_id: int) -> Comic:
        """ Obtiene un comic de Marvel. """
        URL = f"{self._settings.URL_RECORDS}/{comic_id}"
        coroutine = self._general_request.get(URL)
        response = asyncio.run(coroutine)

        if not response['response']:
            if response['type_error'] == 'timeout':
                raise ErrorResponse(**self._error_attributes(103))
            raise ErrorResponse(**self._error_attributes(102))

        adds: dict = response['additionals']

        if not response['success']:
            data = response['response']['data']
            status = response['status']
            message = data.get('user_message', '')
            self._request_log_error(adds['url'], message, adds['time_elapsed'],
                                    adds['reason'], 'GET')
            raise ErrorResponse(None, message, self.transaction_id, status)

        self._request_log_info(adds['url'], "Success getting comic data.",
                               adds['time_elapsed'], 'GET')

        comic = response['response']['data'].get('comic')
        if not comic:
            message = f"Comic '{comic_id}' Not Found"
            self._request_log_error(adds['url'], message, adds['time_elapsed'],
                                    message, 'GET')
            raise ErrorResponse(None, message, self.transaction_id, 404)

        comic = Comic.parse_obj(comic)
        return comic

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self._general_request.log = self._log_external
        self.__db_service.log = self._log_external
