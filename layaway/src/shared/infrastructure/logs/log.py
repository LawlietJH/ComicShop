import json
import socket
from datetime import datetime

from log4python.Log4python import log

from shared.infrastructure.settings import get_settings

from .measurement import Measurement

settings = get_settings()


class Log:
    log_file = log()

    def __init__(self, tracing_id: str = None, origin: str = 'INTERNAL'):
        self.level = 'INFO'
        self.schema_version = settings.VERSION_LOG
        self.log_origin = origin
        self.timestamp = self.get_timestamp()
        self.tracing_id = tracing_id
        self.hostname = socket.gethostname()
        self.service = settings.SERVICE_NAME
        self.appname = settings.APP_NAME
        self.total_time = None
        self.message = None
        self.measurement = None
        self.object = None
        self.stacktrace = None
        self._init_time = self.get_timestamp()

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def __str__(self):
        return self.__getself__().__str__()

    def __getself__(self):
        return json.dumps({
            key: value
            for key, value in self.__dict__.items()
            if value is not None and not key.startswith('_')
        }, ensure_ascii=False)

    def __setstacktrace__(self, error, method):
        now = datetime.now()
        self.stacktrace = {
            'timestamp': datetime.timestamp(now),
            'level': 'ERROR',
            'thread': method,
            'message': str(error)
        }

    def get_time_ms(self):
        return int((datetime.now() - datetime.strptime(
            self._init_time, "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000)

    def add_measurement(self, measurement: dict):
        self.measurement = measurement

    def add_object(self, object: dict):
        self.object = object

    def info(self, message, object: dict = None,
             measurement: Measurement = None):
        self.level = 'INFO'
        if measurement is not None:
            self.measurement = measurement.get_service()
        else:
            self.measurement = measurement
        self.object = object
        self.message = message
        self.stacktrace = None
        self.total_time = self.get_time_ms()
        self.timestamp = self.get_timestamp()
        self.log_file.info(self.__getself__())

    def error(self, message: str, method: str = '',
              error: str | Exception = '', object: dict = None,
              measurement: Measurement = None):
        self.level = 'ERROR'
        if method or error:
            self.__setstacktrace__(error, method)
        else:
            self.stacktrace = None
        if measurement is not None:
            self.measurement = measurement.get_service()
        else:
            self.measurement = measurement
        self.object = object
        self.message = message
        self.total_time = self.get_time_ms()
        self.timestamp = self.get_timestamp()
        self.log_file.error(self.__getself__())
