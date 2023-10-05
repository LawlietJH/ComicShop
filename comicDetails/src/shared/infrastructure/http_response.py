from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from shared.domain.response import Response


class HttpResponse(JSONResponse):
    """
    Class used to obtain and return valid http responses according to our
    standard.

    Parameters:
        status_code: integer with status code to return
        content: content of the response
    """
    def __init__(self, status_code: int, content: Response,
                 excludes: set = None, *args, **kwargs) -> None:
        if excludes is None:
            excludes = {}
        content_data = jsonable_encoder(content, exclude=excludes)
        super().__init__(
            content=content_data,
            status_code=status_code,
            *args, **kwargs,
        )

class WorkerResponse(HttpResponse):
    def __init__(self, content: Response) -> None:
        super().__init__(
            content=content,
            status_code=content._status_code,
            excludes={'_status_code'}
        )
