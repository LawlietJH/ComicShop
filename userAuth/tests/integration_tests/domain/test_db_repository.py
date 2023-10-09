import uuid

import pytest

from shared.infrastructure.logs import Log
from worker.domain.db_repository import DBRepository


@pytest.mark.db_repository
@pytest.mark.domain
class TestIntegrationDBRepository:
    log = Log(str(uuid.uuid4()))

    def test_class(self, mocker):
        mocker.patch.multiple(DBRepository, __abstractmethods__=set())
        repository = DBRepository()
        with pytest.raises(NotImplementedError):
            repository.is_alive(self.log)
        with pytest.raises(NotImplementedError):
            repository.get_error_details(self.log)
