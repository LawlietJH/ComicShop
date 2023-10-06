import uuid

import pytest

from shared.domain.response import MetadataResponse
from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from shared.infrastructure.settings import get_settings
from worker.application import DBWorkerService, UpdateCacheUseCase
from worker.infrastructure.mongo_worker_repository import MongoWorkerRepository


@pytest.mark.usecases
@pytest.mark.application
class TestIntegrationUpdateCacheUseCase:
    log = Log(str(uuid.uuid4()))
    settings = get_settings()
    mongo_db = MongoDatabase(
        db_uri=settings.MONGO_URI,
        app_name=settings.SERVICE_NAME,
        max_pool_size=settings.MONGO_MAX_POOL_SIZE,
        timeout=settings.MONGO_TIMEOUT_MS)
    repository = MongoWorkerRepository(
        session_factory=mongo_db.session)
    db_worker_service = DBWorkerService(repository)

    def test_execute(self):
        use_case = UpdateCacheUseCase(
            self.db_worker_service, self.log, self.settings)
        data = use_case.execute()
        assert data._status_code == 200
        assert data.data['status'] == 'Successful'
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, MetadataResponse)
        assert 'status' in data.data
