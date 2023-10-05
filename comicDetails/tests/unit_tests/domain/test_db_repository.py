import pytest

from shared.infrastructure.logs import Log
from worker.domain.db_repository import DBRepository


@pytest.mark.domain
@pytest.mark.db_repository
class TestUnitDBRepository:

    def test_class(self, mocker):
        mocker.patch.multiple(DBRepository, __abstractmethods__=set())
        log = mocker.patch.object(Log, '__init__')
        repository = DBRepository()
        with pytest.raises(NotImplementedError):
            repository.is_alive(log)
        with pytest.raises(NotImplementedError):
            repository.get_general_config(log)
        with pytest.raises(NotImplementedError):
            repository.get_service_config(log)
        with pytest.raises(NotImplementedError):
            repository.get_error_details(log)

    # TODO: It is necessary to add a test class file for each repository that
    #  your service requires. Do not forget to test each of your new functions
