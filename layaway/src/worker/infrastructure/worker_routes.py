import autodynatrace
from ddtrace import tracer
from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from shared.infrastructure import HttpResponse
from shared.infrastructure.settings import get_settings
from worker.domain import (responses_layaway, responses_liveness,
                           responses_readiness)
from worker.domain.entities import Filter, Layaway
from worker.infrastructure import WorkerController

# layaway: /orders/api/v1/layaway/docs

settings = get_settings()

version = settings.API_VERSION
namespace = settings.NAMESPACE
resource = settings.RESOURCE
prefix = f'/{namespace}/api/{version}/{resource}'

descriptions = {
    'liveness': "Verifica que el servicio se encuentre disponible.",
    'readiness': "Verifica que existan conexiones activas a MONGO/REDIS/FIREBASE.",
    'set_layaway': "Agrega un cómic al apartado.",
    'get_layaway': "Obtiene el apartado de cómics del usuario."
}

router = APIRouter(prefix=prefix)


@router.get('/liveness', tags=['Health Checks'], responses=responses_liveness,
            summary=descriptions['liveness'])
@autodynatrace.trace(f'{prefix}/liveness')
@tracer.wrap(service='userauth', resource=f'GET {prefix}/liveness')
def liveness() -> dict:
    return {'status': 'Success'}


@router.get('/readiness', tags=["Health Checks"], responses=responses_readiness,
            summary=descriptions['readiness'])
@autodynatrace.trace(f'{prefix}/readiness')
@tracer.wrap(service='userauth', resource=f'GET {prefix}/liveness')
def readiness() -> HttpResponse:
    return WorkerController.readiness()


@router.post(f'', tags=["Layaway"], responses=responses_layaway,
             summary=descriptions['set_layaway'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='userauth', resource=f'POST {prefix}/{resource}')
def set_layaway(body: Layaway,
                authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> HttpResponse:
    """ Agrega un cómic al apartado. """
    token = authorization.credentials
    return WorkerController.set_layaway(token, body)


@router.get(f'', tags=["Layaway"], responses=responses_layaway,
            summary=descriptions['get_layaway'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='userauth', resource=f'GET {prefix}/{resource}')
def get_layaway(filter: Filter = Depends(),
                authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> HttpResponse:
    """ Obtiene el apartado de cómics del usuario. """
    token = authorization.credentials
    return WorkerController.get_layaway(token, filter)
