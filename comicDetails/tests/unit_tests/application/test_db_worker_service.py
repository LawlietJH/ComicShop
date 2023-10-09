import pytest
from worker.infrastructure import MongoWorkerRepository
from worker.application import DBWorkerService


@pytest.mark.application
@pytest.mark.services
class TestUnitDBWorkerService:

    def test_class(self, mocker, test_data):
        repository = mocker.patch.object(MongoWorkerRepository, '__init__')
        repository.is_alive = mocker.MagicMock(return_value=True)
        repository.upsert_micro_service = mocker.MagicMock(return_value={
            'data': {'nModified': 0}, 'status': 'success'})
        repository.get_error_details = mocker.MagicMock(
            return_value=test_data.get('error_details')['errors'])
        db_worker_service = DBWorkerService(repository)
        is_alive = db_worker_service.is_alive()
        error_details = db_worker_service.get_error_details()
        assert isinstance(is_alive, bool)
        assert is_alive
        assert isinstance(error_details, dict)
