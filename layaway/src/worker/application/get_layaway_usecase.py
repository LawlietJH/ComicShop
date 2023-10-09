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
from worker.domain.entities import Filter, User

from .functionalities import Functionalities


class GetLayawayUseCase(Functionalities):
    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._general_request = GeneralRequestServer()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('GetLayawayUseCase - execute')
    @tracer.wrap(service='layaway', resource='execute')
    def execute(self, token: str, filter: Filter) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        object_ = {'token': token, 'order_by': filter.order_by}
        self._log.info("Start: GET /layaway", object_)

        layaway = self._get_data(token, filter)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)
        self._log.info("Get Layaway Successfully")

        return SuccessResponse(layaway, 200, self.transaction_id, total_time_elapsed)

    def _get_data(self, token: str, filter: Filter) -> dict:
        user = self._get_user(token)
        layaway = {'user_id': user.id,
                   'username': user.username,
                   'layaway': []}

        layaway_data = self.__db_service.get_layaway(user_id=user.id)

        if layaway_data is None:
            raise ErrorResponse(None, "Error getting layaway",
                                self.transaction_id, 500)
        elif not layaway_data:
            return layaway

        layaway_data = layaway_data['layaway']

        if filter.order_by == 'id':
            layaway_data = sorted(layaway_data, reverse=filter.reverse,
                                  key=lambda item: item['id'])
        elif filter.order_by == 'date':
            layaway_data = sorted(layaway_data, reverse=filter.reverse,
                                  key=lambda item: item['on_sale_date'])
        elif filter.order_by in ('title', 'name'):
            layaway_data = sorted(layaway_data, reverse=filter.reverse,
                                  key=lambda item: item['title'])

        layaway['layaway'] = layaway_data

        return layaway

    # General Request ----------------------------------------------------------

    @autodynatrace.trace('GetLayawayUseCase - _get_user')
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

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self.__db_service.log = self._log_external
