import uuid

import pytest

from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from shared.infrastructure.settings import get_settings
from worker.application import DBWorkerService
from worker.infrastructure.mongo_worker_repository import MongoWorkerRepository


@pytest.mark.application
@pytest.mark.services
class TestIntegrationWorkerService:
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
    db_worker_service.log = log

    def test_class(self):
        is_alive = self.db_worker_service.is_alive()
        general_config = self.db_worker_service.get_general_config()
        service_config = self.db_worker_service.get_service_config()
        error_details = self.db_worker_service.get_error_details()
        assert is_alive
        assert isinstance(is_alive, bool)
        assert isinstance(general_config, dict)
        assert isinstance(service_config, dict)
        assert isinstance(error_details, dict)
        assert 'environment' in general_config
