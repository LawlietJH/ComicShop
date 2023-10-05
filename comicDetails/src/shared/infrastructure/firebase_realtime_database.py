from collections.abc import Iterator
from contextlib import contextmanager, suppress

import firebase_admin
from firebase_admin import credentials, db, exceptions

from shared.domain.database import Database, Session

from .utils import Utils


class FirebaseRealTimeSession(Session):
    def __init__(self, default_db: str, key_path: str, timeout: int) -> None:
        self._auth_certificate = key_path
        self._http_timeout = timeout
        self._default_db = default_db

    def __enter__(self):
        return self

    def get_app(self, db_url: str, use_override: bool = False,
                override_params: dict = None) -> firebase_admin.App:
        if not firebase_admin._apps.get(db_url):
            auth_parameters = {
                'databaseURL': db_url,
                'httpTimeout': self._http_timeout
            }
            if use_override:
                auth_parameters['databaseAuthVariableOverride'] = override_params
            auth_credentials = credentials.Certificate(self._auth_certificate) 
            firebase_admin.initialize_app(auth_credentials, auth_parameters, db_url)
        return firebase_admin._apps.get(db_url)

    def is_alive(self) -> dict:
        data = {
            'status': True,
            'message': 'Success',
            'method': Utils.get_method_name(self, 'is_alive')
        }
        try:
            app = self.get_app(self._default_db)
            reference = db.reference('terms', app)
            reference.get()
        except (exceptions.FirebaseError, Exception) as ex:
            data['status'] = False
            data['message'] = str(ex)
        return data


class FirebaseRealTimeDatabase(Database):
    def __init__(self, default_db: str, key_path: str, timeout: int) -> None:
        self.__session = FirebaseRealTimeSession(default_db, key_path, timeout)

    @contextmanager
    def session(self) -> Iterator[Session]:
        with suppress(Exception):
            yield self.__session
