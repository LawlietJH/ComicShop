import asyncio
import copy
import time
import uuid

import autodynatrace
from ddtrace import tracer
from shared.domain import FailureResponse, Response, SuccessResponse
from shared.infrastructure import ErrorResponse, GeneralRequestServer, Settings
from shared.infrastructure.logs import Log
from shared.infrastructure.utils import Utils
from worker.domain import DBRepository
from worker.domain.entities import Character, Comic

from .functionalities import Functionalities


class GetRecordUseCase(Functionalities):

    def __init__(self, db_worker_service: DBRepository,
                 log: Log, settings: Settings) -> None:
        self.__db_service = db_worker_service
        self._log = log
        self._settings = settings
        self._general_request = GeneralRequestServer()
        self.transaction_id = str(uuid.uuid4())
        self.init_time = time.perf_counter()

    @autodynatrace.trace('GetRecordUseCase - execute')
    @tracer.wrap(service='comicdetails', resource='execute')
    def execute(self, id: int) -> Response:
        self._set_logs()
        self._set_configs(self.__db_service)

        self._log.info("Start: /comics", object={'id': id})

        data = self._get_record(id)

        total_time_elapsed = Utils.get_time_elapsed_ms(self.init_time)

        self._log.info("Get Comics: Success")

        return SuccessResponse(data, 200, self.transaction_id, total_time_elapsed)

    def _get_record(self, id: int):
        data = {}

        url_characters = self._get_url(id=id)
        url_comics = self._get_url(type_url='comics', id=id)

        comic_item = self._get_marvel_data(url_comics)
        character_item = self._get_marvel_data(url_characters)

        if comic_item:
            comic = Comic.parse_obj({
                'id': comic_item['id'],
                'title': comic_item['title'],
                'image': f"{comic_item['thumbnail']['path']}.{comic_item['thumbnail']['extension']}",
                'on_sale_date': [obj['date'] for obj in comic_item['dates'] if obj.get('type') == 'onsaleDate'].pop()
            })
            data['comic'] = comic

        elif character_item:
            character = Character.parse_obj({
                'id': character_item['id'],
                'name': character_item['name'],
                'image': f"{character_item['thumbnail']['path']}.{character_item['thumbnail']['extension']}",
                'appearances': character_item['comics']['available']
            })
            data['character'] = character
        else:
            raise ErrorResponse(None, f"Personaje o Comic con el id '{id}' no encontrado.",
                                self.transaction_id, 404)

        return data

    # General Request ----------------------------------------------------------

    @autodynatrace.trace('GetRecordUseCase - _get_marvel_data')
    @tracer.wrap(service='comicdetails', resource='_get_marvel_data')
    def _get_marvel_data(self, url: str):
        """ Obtiene los personajes de Marvel por paginado. """
        coroutine = self._general_request.get(url)
        response = asyncio.run(coroutine)

        if not response['response']:
            if response['type_error'] == 'timeout':
                raise ErrorResponse(**self._error_attributes(103))
            raise ErrorResponse(**self._error_attributes(102))

        adds: dict = response['additionals']

        if not response['success']:
            user_message = "Error al consumir el recurso externo"
            self._request_log_error(adds['url'], user_message, adds['time_elapsed'],
                                    adds['reason'], 'GET')
            return

        self._request_log_info(adds['url'], "Success getting characters data.",
                               adds['time_elapsed'], 'GET')

        return response['response']['data']['results'][0]

    # General Functions --------------------------------------------------------

    def _set_logs(self):
        self._log.tracing_id = self.transaction_id
        self._log_external = copy.deepcopy(self._log)
        self._log_external.log_origin = 'EXTERNAL'
        self._general_request.log = self._log_external