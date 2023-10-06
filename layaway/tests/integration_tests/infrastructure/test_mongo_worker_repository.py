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

    def test_is_not_alive(self):
        mongo_db = MongoDatabase(
            db_uri=self.settings.MONGO_URI.replace('27017', '27018'),
            app_name=self.settings.SERVICE_NAME,
            max_pool_size=self.settings.MONGO_MAX_POOL_SIZE,
            timeout=self.settings.MONGO_TIMEOUT_MS)
        repository = MongoWorkerRepository(
            session_factory=mongo_db.session)
        assert not repository.is_alive(self.log)

    def test_general_config(self):
        general_config = self.repository.get_general_config(self.log)
        environment = general_config[general_config['environment']]
        assert isinstance(general_config, dict)
        assert isinstance(environment, dict)
        assert 'timeout' in general_config
        assert 'timeout_internos' in general_config
        assert 'reconexion' in general_config
        assert 'storeId' in general_config
        assert 'environment' in general_config
        assert 'wcs_endpoint' in environment

    def test_service_config(self):
        service_config = self.repository.get_service_config(self.log)
        assert isinstance(service_config, dict)

    def test_error_details(self):
        errors = self.repository.get_error_details(self.log)
        assert isinstance(errors, dict)

    # TODO: It is necessary to add a test for each of your new functions here
