import pytest

from shared.infrastructure.logs import Log
from shared.infrastructure.settings import Settings
from shared.domain.response import MetadataResponse
from worker.application import DBWorkerService, ReadinessUseCase


@pytest.mark.application
@pytest.mark.usecases
class TestUnitReadinessUseCase:
    db_worker_service: DBWorkerService = None
    use_case: ReadinessUseCase = None
    settings: Settings = None
    log: Log = None

    def init_mocks(self, mocker):
        self.db_worker_service = mocker.patch.object(
            DBWorkerService, '__init__')
        self.log = mocker.patch.object(Log, '__init__')
        self.settings = mocker.patch.object(Settings, '__init__')
        self.use_case = ReadinessUseCase(self.db_worker_service, self.log,
                                         settings=self.settings)

    def test_execute(self, mocker):
        self.init_mocks(mocker)
        data = self.use_case.execute()
        assert data._status_code == 200
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, MetadataResponse)
        assert 'status' in data.data
        assert data.data['status'] == 'Mongo is alive'

    def test_execute_not_alive(self, mocker):
        self.init_mocks(mocker)
        self.db_worker_service.is_alive = mocker.MagicMock(return_value=False)
        data = self.use_case.execute()
        assert data._status_code == 500
        assert isinstance(data.data, dict)
        assert isinstance(data.meta, MetadataResponse)
        assert 'user_message' in data.data
        assert data.data['user_message'] == 'Error de conexión a mongo'

    # TODO: It is necessary to add a test class file for each use case that
    #  your service requires.
