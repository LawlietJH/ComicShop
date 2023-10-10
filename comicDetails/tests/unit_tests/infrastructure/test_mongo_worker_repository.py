import pytest

from shared.infrastructure import MongoDatabase
from shared.infrastructure.logs import Log
from tests.unit_tests.utils.mongo_mock import MongoMock
from worker.infrastructure.mongo_worker_repository import MongoWorkerRepository


@pytest.mark.infrastructure
@pytest.mark.repositories
class TestUnitMongoWorkerRepository:
    mongo_db: MongoDatabase = None
    log: Log = None
    session = None

    def init_mocks(self, mocker):
        self.mongo_db = mocker.patch.object(MongoDatabase, '__init__')
        self.log = mocker.patch.object(Log, '__init__')
        self.session = mocker.MagicMock()

    def test_is_alive(self, mocker):
        self.init_mocks(mocker)
        self.session.return_value.__enter__.return_value.is_alive. \
            return_value = {'status': True, 'message': 'Success',
                            'method': 'MongoSession.is_alive'}
        repository = MongoWorkerRepository(
            session_factory=self.session)
        is_alive = repository.is_alive(self.log)
        assert isinstance(is_alive, bool)
        assert is_alive

    def test_is_not_alive(self, mocker):
        self.init_mocks(mocker)
        self.session.return_value.__enter__.return_value.is_alive. \
            return_value = {'status': False, 'message': 'Error',
                            'method': 'MongoSession.is_alive'}
        repository = MongoWorkerRepository(
            session_factory=self.session)
        is_alive = repository.is_alive(self.log)
        assert isinstance(is_alive, bool)
        assert not is_alive

    def test_get_error_details(self, mocker, test_data):
        self.init_mocks(mocker)
        self.session.return_value.__enter__. \
            return_value.get_db. \
            return_value.configs. \
            find_one.return_value = test_data.get('error_details')

        repository = MongoWorkerRepository(
            session_factory=self.session)
        errors = repository.get_error_details(self.log, **{'test': True})
        assert isinstance(errors, dict)
        assert len(errors) > 0
