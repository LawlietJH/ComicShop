from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # App Configurations
    APP_NAME: str = 'appcoppel'
    SERVICE_NAME: str
    NAMESPACE: str
    API_VERSION: str
    RESOURCE: str
    IMAGE_VERSION: str
    ENABLE_DOCS: bool = False
    PORT: int = 8000
    RELOAD: bool = False
    # Mongo
    MONGO_URI: str
    MONGO_DB_NAME: str = 'configuraciones_appcom'
    MONGO_TIMEOUT_MS: int = 500
    MONGO_MAX_POOL_SIZE: int = 20
    MONGO_ID_GLOBAL_CONFIG: str = 'globalConfig'
    MONGO_ID_GENERAL_CONFIG: str = 'general'
    MONGO_ID_ERROR_DETAILS: str = 'errorDetails'
    MONGO_ID_SERVICE_CONFIG: str
    # Logs
    VERSION_LOG: str = 'v1'
    APPENDERS: str = 'console'
    # Redis
    # TODO: uncomment this if you require 'redis' in your service.
    #  don't forget to look at the requirements file
    REDIS: str
    REDIS_EXPIRATION_MINS: int = 1440
    # Firebase
    # TODO: uncomment this if you require 'Firebase' in your service.
    #  don't forget to look at the requirements file
    FIREBASE_KEY_PATH: str
    FIREBASE_DEFAULT_DB: str
    FIREBASE_TIMEOUT_SEC: int = 5
    # Http
    # TODO: uncomment this if you require 'GeneralRequest' in your service.
    #  don't forget to look at the requirements file
    DEVELOPER_PORTAL_HTTP_ERRORS: str
    HTTP_TIMEOUT_SEC: int = 15
    # Otros
    STORE_ID: int = 10151


@lru_cache()
def get_settings() -> Settings:
    return Settings()
