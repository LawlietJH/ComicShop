from datetime import datetime

from shared.infrastructure.settings import get_settings
from shared.infrastructure.utils import Utils

settings = get_settings()


class MetadataResponse:
    """
    Class that generates the metadata for the responses that will return the
    requests made to the service.

    Parameters:
        transaction_id: string in uuid4 format with the unique transaction id
        time_elapsed: transaction time in milliseconds

    Attributes:
        timestamp: time at which the transaction occurs
    """
    transaction_id: str
    timestamp: datetime.now
    time_elapsed: int | float = None

    def __init__(self, transaction_id: str, time_elapsed: int | float = None,
                 **kwargs) -> None:
        self.transaction_id = transaction_id
        self.timestamp = datetime.now()
        self.time_elapsed = time_elapsed
        Utils.add_attributes(self, kwargs)
        Utils.discard_empty_attributes(self)
        Utils.sort_attributes(self)


class Response:
    """
    Class that generates the general response for requests to the microservice

    Parameters:
        data: dictionary with the information that the transaction has generated
        meta: metadata of the request
    """
    data: dict
    meta: MetadataResponse

    def __init__(self, data: dict, meta: MetadataResponse) -> None:
        self.data = data
        self.meta = meta


class SuccessResponse(Response):
    def __init__(self, data: dict, status_code: int, transaction_id: str,
                 time_elapsed: int | float, **kwargs) -> None:
        self._status_code = status_code
        meta = MetadataResponse(transaction_id, time_elapsed, **kwargs)
        super().__init__(data, meta)


class FailureResponse(Response):
    def __init__(self, data: dict, status_code: int, transaction_id: str,
                 **kwargs) -> None:
        self._status_code = status_code
        meta = MetadataResponse(transaction_id, **kwargs)
        super().__init__(data, meta)
