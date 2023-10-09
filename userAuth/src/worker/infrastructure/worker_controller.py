import autodynatrace
import container
from ddtrace import tracer
from shared.infrastructure import WorkerResponse
from worker.application import (LoginUseCase, ReadinessUseCase, SingupUseCase,
                                UpdateCacheUseCase, ValidateTokenUseCase)
from worker.domain.entities import UserLogin, UserRegistration


class WorkerController:
    @staticmethod
    @autodynatrace.trace('WorkerController - readiness')
    @tracer.wrap(service='userauth', resource='readiness')
    def readiness():
        with container.SingletonContainer.scope() as app:
            use_case: ReadinessUseCase = app.use_cases.readiness()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - update_cache')
    @tracer.wrap(service='userauth', resource='update_cache')
    def update_cache():
        with container.SingletonContainer.scope() as app:
            use_case: UpdateCacheUseCase = app.use_cases.update_cache()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - singup')
    @tracer.wrap(service='userauth', resource='singup')
    def singup(user: UserRegistration):
        with container.SingletonContainer.scope() as app:
            use_case: SingupUseCase = app.use_cases.singup()
            data = use_case.execute(user)
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - login')
    @tracer.wrap(service='userauth', resource='login')
    def login(user: UserLogin):
        with container.SingletonContainer.scope() as app:
            use_case: LoginUseCase = app.use_cases.login()
            data = use_case.execute(user)
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - validate_token')
    @tracer.wrap(service='userauth', resource='validate_token')
    def validate_token(token: str):
        with container.SingletonContainer.scope() as app:
            use_case: ValidateTokenUseCase = app.use_cases.validate_token()
            data = use_case.execute(token)
            return WorkerResponse(content=data)
