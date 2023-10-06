import autodynatrace
import container
from ddtrace import tracer
from shared.infrastructure import WorkerResponse
from worker.application import (GetRecordsUseCase, GetRecordUseCase,
                                ReadinessUseCase, UpdateCacheUseCase)
from worker.domain.entities import Filter


class WorkerController:
    @staticmethod
    @autodynatrace.trace('WorkerController - readiness')
    @tracer.wrap(service='comicdetails', resource='readiness')
    def readiness():
        with container.SingletonContainer.scope() as app:
            use_case: ReadinessUseCase = app.use_cases.readiness()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - update_cache')
    @tracer.wrap(service='comicdetails', resource='update_cache')
    def update_cache():
        with container.SingletonContainer.scope() as app:
            use_case: UpdateCacheUseCase = app.use_cases.update_cache()
            data = use_case.execute()
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - get_records')
    @tracer.wrap(service='comicdetails', resource='get_records')
    def get_records(filter: Filter):
        with container.SingletonContainer.scope() as app:
            use_case: GetRecordsUseCase = app.use_cases.get_records()
            data = use_case.execute(filter)
            return WorkerResponse(content=data)

    @staticmethod
    @autodynatrace.trace('WorkerController - get_record')
    @tracer.wrap(service='comicdetails', resource='get_record')
    def get_record(id: int):
        with container.SingletonContainer.scope() as app:
            use_case: GetRecordUseCase = app.use_cases.get_record()
            data = use_case.execute(id)
            return WorkerResponse(content=data)
