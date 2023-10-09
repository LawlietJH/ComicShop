from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # App Configurations
    APP_NAME: str = 'ComicShop'
    SERVICE_NAME: str = 'userAuth'
    NAMESPACE: str = 'users'
    API_VERSION: str = 'v1'
    IMAGE_VERSION: str = '1.0.0'
    ENABLE_DOCS: bool = False
    PORT: int = 8000
    RELOAD: bool = False
    # Mongo
    MONGO_URI: str
    MONGO_DB_NAME: str = 'configs'
    MONGO_DB_NAME_USERS: str = 'users'
    MONGO_TIMEOUT_MS: int = 500
    MONGO_MAX_POOL_SIZE: int = 20
    MONGO_ID_ERROR_DETAILS: str = 'errorDetails'
    # Logs
    VERSION_LOG: str = 'v1'
    APPENDERS: str = 'console'
    # Http
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    DEVELOPER_PORTAL_HTTP_ERRORS: str = 'https://developer-app.com/errors'
    HTTP_TIMEOUT_SEC: int = 15


@lru_cache()
def get_settings() -> Settings:
    return Settings()
