import autodynatrace
from ddtrace import tracer

import container
from shared.infrastructure import WorkerResponse
from worker.application import (HelloWorldUseCase, ReadinessUseCase,
                                UpdateCacheUseCase)


class WorkerController:
    @staticmethod
    @autodynatrace.trace('WorkerController - readiness')
    @tracer.wrap(service='basetemplate', resource='readiness')
    def readiness():
        with container.SingletonContainer.scope() as app:
            use_case: ReadinessUseCase = app.use_cases.readiness()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - update_cache')
    @tracer.wrap(service='basetemplate', resource='update_cache')
    def update_cache():
        with container.SingletonContainer.scope() as app:
            use_case: UpdateCacheUseCase = app.use_cases.update_cache()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - hello_world')
    @tracer.wrap(service='basetemplate', resource='hello_world')
    def hello_world(env: str = ''):
        with container.SingletonContainer.scope() as app:
            use_case: HelloWorldUseCase = app.use_cases.hello_world()
            data = use_case.execute(env)
            return WorkerResponse(content=data)
