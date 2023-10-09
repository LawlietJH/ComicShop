import uuid

import pytest

from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from shared.infrastructure.settings import get_settings
from worker.infrastructure.mongo_worker_repository import MongoWorkerRepository


@pytest.mark.infrastructure
@pytest.mark.repositories
class TestIntegrationMongoWorkerRepository:
    log = Log(str(uuid.uuid4()))
    settings = get_settings()
    mongo_db = MongoDatabase(
        db_uri=settings.MONGO_URI,
        app_name=settings.SERVICE_NAME,
        max_pool_size=settings.MONGO_MAX_POOL_SIZE,
        timeout=settings.MONGO_TIMEOUT_MS)
    repository = MongoWorkerRepository(
        session_factory=mongo_db.session)

    def test_is_alive(self):
        assert self.repository.is_alive(self.log)

    def test_error_details(self):
        errors = self.repository.get_error_details(self.log)
        assert isinstance(errors, dict)
