import uuid

import pytest

from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from shared.infrastructure.settings import get_settings
from worker.application import DBWorkerService, ReadinessUseCase
from worker.infrastructure.mongo_worker_repository import MongoWorkerRepository


@pytest.mark.usecases
@pytest.mark.application
class TestIntegrationReadinessUseCase:
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
        use_case = ReadinessUseCase(
            self.db_worker_service, self.log, self.settings)
        data = use_case.execute()
        assert data._status_code == 200
        assert data.data['status'] == 'Mongo is alive'
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, object)
        assert 'status' in data.data

    def test_not_alive(self):
        self.mongo_db = MongoDatabase(
            db_uri=self.settings.MONGO_URI.replace('27017', '27018'),
            app_name=self.settings.SERVICE_NAME,
            max_pool_size=self.settings.MONGO_MAX_POOL_SIZE,
            timeout=self.settings.MONGO_TIMEOUT_MS)
        self.repository = MongoWorkerRepository(
            session_factory=self.mongo_db.session)
        self.db_worker_service = DBWorkerService(self.repository)
        use_case = ReadinessUseCase(
            self.db_worker_service, self.log, self.settings)
        data = use_case.execute()
        assert data._status_code == 500
        assert data.data['user_message'] == 'Error de conexión a mongo'
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, object)
        assert 'user_message' in data.data

    # TODO: It is necessary to add a test class file for each use case that
    #  your service requires.
