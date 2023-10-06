from abc import abstractmethod
from contextlib import AbstractContextManager, contextmanager
from typing import Any, Callable


class Session:
    pass


class Database:
    @abstractmethod
    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Any]]:
        pass
