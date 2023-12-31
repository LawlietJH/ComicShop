import autodynatrace
from ddtrace import tracer
from fastapi import APIRouter, Depends, Header
from shared.infrastructure import HttpResponse
from shared.infrastructure.settings import get_settings
from worker.domain import (responses_get_records, responses_liveness,
                           responses_readiness)
from worker.domain.entities import Filter
from worker.infrastructure import WorkerController

# comicDetails: /catalogs/api/v1/records/docs

settings = get_settings()

version = settings.API_VERSION
namespace = settings.NAMESPACE
resource = settings.RESOURCE
prefix = f'/{namespace}/api/{version}/{resource}'

descriptions = {
    'liveness': "Verifica que el servicio se encuentre disponible.",
    'readiness': "Verifica que existan conexiones activas a MONGO/REDIS/FIREBASE.",
    'get_records': "Devuelve un listado de personajes o comics.",
    'get_record': "Devuelve un personaje o un comic por ID."
}

router = APIRouter(prefix=prefix)


@router.get('/liveness', tags=['Health Checks'], responses=responses_liveness,
            summary=descriptions['liveness'])
@autodynatrace.trace(f'{prefix}/liveness')
@tracer.wrap(service='comicdetails', resource=f'GET {prefix}/liveness')
def liveness() -> dict:
    return {'status': 'Success'}


@router.get('/readiness', tags=["Health Checks"], responses=responses_readiness,
            summary=descriptions['readiness'])
@autodynatrace.trace(f'{prefix}/readiness')
@tracer.wrap(service='comicdetails', resource=f'GET {prefix}/liveness')
def readiness() -> HttpResponse:
    return WorkerController.readiness()


@router.get('', tags=["Comics"], responses=responses_get_records,
            summary=descriptions['get_records'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='comicdetails', resource=f'GET {prefix}')
def get_records(filter: Filter = Depends()) -> HttpResponse:
    """ Devuelve todo un listado de personajes y/o comics. """
    return WorkerController.get_records(filter)


@router.get('/{id}', tags=["Comics"], responses=responses_get_records,
            summary=descriptions['get_record'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='comicdetails', resource=f'GET {prefix}/id')
def get_record(id: int) -> HttpResponse:
    """ Devuelve un personaje o un comic por su ID. """
    return WorkerController.get_record(id)
