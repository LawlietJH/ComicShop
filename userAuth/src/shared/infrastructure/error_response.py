import contextlib

from .settings import get_settings

settings = get_settings()


class ErrorResponse(Exception):
    def __init__(
            self, error_code: int | str, message: str, transaction_id: str,
            status_code: int = 500, info: str = None, reference_code: str =
            None, **kwargs) -> None:
        if isinstance(error_code, str):
            with contextlib.suppress(Exception):
                error_code = int(error_code)
        self.status_code = status_code
        self.data = {
            'user_message': message
        }
        self.meta = {
            'error_code': error_code,
            'info': info,
            'reference_code': reference_code,
            'transaction_id': transaction_id,
            **kwargs
        }
