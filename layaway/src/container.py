from contextlib import contextmanager
from typing import Optional

from dependency_injector import containers, providers
from shared.infrastructure import MongoDatabase, Settings
from shared.infrastructure.logs import Log
from worker.application import (DBWorkerService, ReadinessUseCase,
                                SetLayawayUseCase, UpdateCacheUseCase)
from worker.infrastructure import MongoWorkerRepository


class RepositoriesContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(Settings)
    mongo_db = providers.Singleton(
        MongoDatabase,
        db_uri=settings.provided.MONGO_URI,
        app_name=settings.provided.SERVICE_NAME,
        max_pool_size=settings.provided.MONGO_MAX_POOL_SIZE,
        timeout=settings.provided.MONGO_TIMEOUT_MS)
    db_worker_repository = providers.Singleton(
        MongoWorkerRepository, session_factory=mongo_db.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    db_worker_service = providers.Factory(
        DBWorkerService,
        db_worker_repository=repositories.db_worker_repository)


class UseCasesContainer(containers.DeclarativeContainer):
    services: ServicesContainer = providers.DependenciesContainer()
    settings = providers.Dependency(Settings)
    log = providers.Factory(Log)
    readiness = providers.Factory(
        ReadinessUseCase, db_worker_service=services.db_worker_service,
        log=log, settings=settings)
    update_cache = providers.Factory(
        UpdateCacheUseCase, db_worker_service=services.db_worker_service,
        log=log, settings=settings)
    set_layaway = providers.Factory(
        SetLayawayUseCase, db_worker_service=services.db_worker_service,
        log=log, settings=settings)


class AppContainer(containers.DeclarativeContainer):
    settings = providers.ThreadSafeSingleton(Settings)
    repositories = providers.Container(
        RepositoriesContainer, settings=settings)
    services = providers.Container(
        ServicesContainer, repositories=repositories)
    use_cases = providers.Container(
        UseCasesContainer, services=services, settings=settings)


class SingletonContainer:
    container: Optional[AppContainer] = None

    @classmethod
    @contextmanager
    def scope(cls):
        try:
            cls.container.services.init_resources()
            yield cls.container
        finally:
            cls.container.services.shutdown_resources()

    @classmethod
    def init(cls) -> None:
        if cls.container is None:
            cls.container = AppContainer()
