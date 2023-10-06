import autodynatrace
from ddtrace import tracer
from fastapi import APIRouter, Depends, Header
from shared.infrastructure import HttpResponse
from shared.infrastructure.settings import get_settings
from worker.domain import (responses_hello_world, responses_liveness,
                           responses_readiness)
from worker.domain.entities import Person
from worker.infrastructure import WorkerController

# serviceName:
# /namespace/v1/resource

settings = get_settings()

version = settings.API_VERSION
namespace = settings.NAMESPACE
resource = settings.RESOURCE
prefix = f'/{namespace}/{version}/{resource}'

descriptions = {
    'liveness': "Verifica que el servicio se encuentre disponible.",
    'readiness': "Verifica que existan conexiones activas a MONGO/REDIS/FIREBASE.",
    'get_comics': "Devuelve un listado de comics.",
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


@router.get('', tags=["Comic"], responses=responses_hello_world,
            summary=descriptions['get_comics'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='comicdetails', resource=f'GET {prefix}')
def get_comics(filter: Person = Depends()) -> HttpResponse:
    """ Devuelve un listado de comics. """
    return WorkerController.get_comics(filter)
