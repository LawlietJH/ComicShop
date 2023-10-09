import datetime
import uuid

import pytest
from fastapi.encoders import jsonable_encoder

from shared.domain.response import MetadataResponse, Response
from shared.infrastructure import Settings
from shared.infrastructure.logs import Log
from worker.application import DBWorkerService, ReadinessUseCase


@pytest.mark.infrastructure
@pytest.mark.controllers
class TestWorkerController:
    db_service: DBWorkerService = None
    log: Log = None
    settings: Settings = None

    def init_mocks(self, mocker):
        self.db_service = mocker.patch.object(DBWorkerService, '__init__')
        self.log = mocker.patch.object(Log, '__init__')

    def test_worker_response(self):
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()
        time_elapsed = 76.47
        data = {
            "response": {
                "nModified": 1
            }
        }
        expected_response = {
            "data": data,
            "meta": {
                "time_elapsed": time_elapsed,
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "transaction_id": transaction_id
            }
        }
        metadata = MetadataResponse(
            transaction_id=transaction_id, timestamp=timestamp,
            time_elapsed=76.47)
        response = Response(data=data, meta=metadata)
        json_response = jsonable_encoder(response)
        assert json_response == expected_response
        assert isinstance(response.meta, MetadataResponse)

    def test_readiness(self, mocker):
        self.init_mocks(mocker)
        readiness = ReadinessUseCase(
            db_worker_service=self.db_service, log=self.log,
            settings=self.settings)
        data = readiness.execute()
        response = jsonable_encoder(data)
        assert 'data' in response
        assert 'meta' in response
        assert isinstance(response, dict)
        assert len(response['data']) > 0
        assert isinstance(response['data'], dict)
        assert len(response['meta']) > 0
        assert isinstance(response['meta'], dict)
