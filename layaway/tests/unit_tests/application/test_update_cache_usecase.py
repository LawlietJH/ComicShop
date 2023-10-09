import pytest

from shared.infrastructure import ErrorResponse, Settings
from shared.infrastructure.logs import Log
from worker.application import DBWorkerService, UpdateCacheUseCase


@pytest.mark.usecases
@pytest.mark.application
class TestUnitUpdateCacheUseCase:
    db_worker_service: DBWorkerService = None
    use_case: UpdateCacheUseCase = None
    settings: Settings = None
    log: Log = None

    def init_mocks(self, mocker):
        self.db_worker_service = mocker.patch.object(
            DBWorkerService, '__init__')
        self.log = mocker.patch.object(Log, '__init__')
        self.settings = mocker.patch.object(Settings, '__init__')
        self.use_case = UpdateCacheUseCase(self.db_worker_service, self.log,
                                           self.settings)

    def test_execute(self, mocker):
        self.init_mocks(mocker)
        data = self.use_case.execute()
        assert data._status_code == 200
        assert data.data['status'] == 'successful'
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, object)
        assert 'status' in data.data

    def test_execute_wrong(self, mocker):
        self.init_mocks(mocker)
        self.db_worker_service.get_error_details = mocker.MagicMock(
            return_value={})
        with pytest.raises(ErrorResponse):
            self.use_case.execute()
