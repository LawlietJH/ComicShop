import autodynatrace
import container
from ddtrace import tracer
from shared.infrastructure import WorkerResponse
from worker.application import (ReadinessUseCase, SetLayawayUseCase,
                                UpdateCacheUseCase)
from worker.domain.entities import Layaway


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
    def set_layaway(token: str, body: Layaway):
        with container.SingletonContainer.scope() as app:
            use_case: SetLayawayUseCase = app.use_cases.set_layaway()
            data = use_case.execute(token, body)
            return WorkerResponse(content=data)
