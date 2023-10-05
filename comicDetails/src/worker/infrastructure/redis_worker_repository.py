import json
import time

from redis import Redis

from shared.infrastructure import Utils
from shared.infrastructure.logs import Log, Measurement
from shared.infrastructure.settings import get_settings
from worker.domain import CacheRepository

settings = get_settings()


class RedisWorkerRepository(CacheRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def is_alive(self, log: Log) -> bool:
        with self.session_factory() as session:

            init_time = time.perf_counter()

            data = session.is_alive()
            success = data.get('status')
            message = data.get('message')
            method_name = data.get('method')

            time_elapsed = Utils.get_time_elapsed_ms(init_time)

            if success:
                measurement = Measurement('Redis', time_elapsed)
                log.info("Redis is alive", measurement=measurement)
            else:
                measurement = Measurement('Redis', time_elapsed, 'Error')
                log.error("Redis is not alive", method=method_name,
                          error=message, measurement=measurement)

            return success

    def get_value(self, key: str, log: Log) -> dict:

        method_name = Utils.get_method_name(self, 'get_value')

        with self.session_factory() as session:

            init_time = time.perf_counter()

            redis: Redis = session.get_connection()
            cache = {}

            try:
                data = redis.get(key)
                time_elapsed = Utils.get_time_elapsed_ms(init_time)
                if data:
                    measurement = Measurement('Redis', time_elapsed)
                    log.info("Get Cache: Successfuly", object={'id': key},
                             measurement=measurement)
                    cache = json.loads(data)
                else:
                    measurement = Measurement('Redis', time_elapsed, 'Error')
                    log.info("Get Cache: Empty", object={'id': key},
                             measurement=measurement)
            except Exception as ex:
                time_elapsed = Utils.get_time_elapsed_ms(init_time)
                measurement = Measurement('Redis', time_elapsed, 'Error')
                log.error("Get Cache: Failed", method=method_name, error=ex,
                          object={'id': key}, measurement=measurement)

            return cache

    def set_value(self, key: str, data: dict, log: Log) -> None:

        method_name = Utils.get_method_name(self, 'set_value')

        with self.session_factory() as session:

            init_time = time.perf_counter()

            redis: Redis = session.get_connection()
            expire = settings.REDIS_EXPIRATION_MINS * 60

            try:
                redis.set(key, json.dumps(data), ex=expire)
                time_elapsed = Utils.get_time_elapsed_ms(init_time)
                measurement = Measurement('Redis', time_elapsed)
                log.info("Set Cache: Successfully",
                         object={'id': key}, measurement=measurement)
            except Exception as ex:
                time_elapsed = Utils.get_time_elapsed_ms(init_time)
                measurement = Measurement('Redis', time_elapsed, 'Error')
                log.error("Set Cache: Failed", method=method_name, error=ex,
                          object={'id': key}, measurement=measurement)
