import autodynatrace
from ddtrace import tracer
from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from shared.infrastructure import HttpResponse
from shared.infrastructure.settings import get_settings
from worker.domain import (responses_liveness, responses_readiness,
                           responses_singup)
from worker.domain.entities import User, UserRegistration
from worker.infrastructure import WorkerController

# serviceName:
# /namespace/v1/resource

settings = get_settings()

version = settings.API_VERSION
namespace = settings.NAMESPACE
prefix = f'/{namespace}/api/{version}'

descriptions = {
    'liveness': "Verifica que el servicio se encuentre disponible.",
    'readiness': "Verifica que existan conexiones activas a MONGO/REDIS/FIREBASE.",
    'singup': "Registra un nuevo usuario.",
    'login': "Inicio de sesión del usuario.",
    'validate_token': "Valida un token y devuelve un payload."
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


@router.post('/singup', tags=["Comics"], responses=responses_singup,
             summary=descriptions['singup'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='userauth', resource=f'POST {prefix}')
def singup(user: UserRegistration) -> HttpResponse:
    """ Registra un usuario. """
    return WorkerController.singup(user)


@router.post('/login', tags=["Comics"], responses=responses_singup,
             summary=descriptions['login'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='userauth', resource=f'POST {prefix}')
def login(user: User) -> HttpResponse:
    """ Obtiene un Token. """
    return WorkerController.login(user)


@router.get('/keys', tags=["Comics"], responses=responses_singup,
            summary=descriptions['validate_token'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='userauth', resource=f'GET {prefix}')
def validate_token(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> HttpResponse:
    """ Valida un Token. """
    token = authorization.credentials
    return WorkerController.validate_token(token)
