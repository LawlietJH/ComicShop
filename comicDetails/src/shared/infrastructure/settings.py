from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # App Configurations
    APP_NAME: str = 'ComicShop'
    SERVICE_NAME: str = 'comicDetails'
    NAMESPACE: str = 'catalogs'
    API_VERSION: str = 'v1'
    RESOURCE: str = 'records'
    IMAGE_VERSION: str = '1.0.0'
    ENABLE_DOCS: bool = False
    PORT: int = 8001
    RELOAD: bool = False
    # Mongo
    MONGO_URI: str
    MONGO_DB_NAME: str = 'users'
    MONGO_TIMEOUT_MS: int = 500
    MONGO_MAX_POOL_SIZE: int = 20
    MONGO_ID_ERROR_DETAILS: str = 'errorDetails'
    # Logs
    VERSION_LOG: str = 'v1'
    APPENDERS: str = 'console'
    # Http
    MARVEL_API_PUBLIC_KEY: str
    MARVEL_API_PRIVATE_KEY: str
    DEVELOPER_PORTAL_HTTP_ERRORS: str = 'http://...'
    HTTP_TIMEOUT_SEC: int = 15


@lru_cache()
def get_settings() -> Settings:
    return Settings()
