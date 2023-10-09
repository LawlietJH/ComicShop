import datetime
import uuid

import pytest
from fastapi.encoders import jsonable_encoder

from shared.domain.response import MetadataResponse, Response
from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from shared.infrastructure.settings import get_settings
from worker.application import DBWorkerService, ReadinessUseCase
from worker.infrastructure import MongoWorkerRepository


@pytest.mark.infrastructure
@pytest.mark.controllers
class TestIntegrationWorkerController:
    log = Log(str(uuid.uuid4()))
    settings = get_settings()
    mongo_db = MongoDatabase(
        db_uri=settings.MONGO_URI,
        app_name=settings.SERVICE_NAME,
        max_pool_size=settings.MONGO_MAX_POOL_SIZE,
        timeout=settings.MONGO_TIMEOUT_MS)
    db_repository = MongoWorkerRepository(mongo_db.session)
    db_service = DBWorkerService(db_repository)
    readiness_use_case = ReadinessUseCase(db_service, log, settings)

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

    def test_readiness(self):
        data = self.readiness_use_case.execute()
        response = jsonable_encoder(data)
        assert 'data' in response
        assert 'meta' in response
        assert 'status' in response['data']
        assert isinstance(response, dict)
        assert len(response['data']) > 0
        assert isinstance(response['data'], dict)
        assert len(response['meta']) > 0
        assert isinstance(response['meta'], dict)
        assert response['_status_code'] == 200
        assert response['data']['status'] == 'Mongo is alive'
