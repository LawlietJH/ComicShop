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
    'get_hello_world': "Responde con un 'Hello World'.",
    'get_hello_person': "Responde un 'Hello World'.",
    'post_hello_person': "Responde con 'Hello World'."
}

router = APIRouter(prefix=prefix)


@router.get('/liveness', tags=['Health Checks'], responses=responses_liveness,
            summary=descriptions['liveness'])
@autodynatrace.trace(f'{prefix}/liveness')
@tracer.wrap(service='basetemplate', resource=f'{prefix}/liveness')
# TODO: You need change the value of 'service' argument to the
# name of the service workload as it appears in rancher.
def liveness() -> dict:
    return {'status': 'Success'}


@router.get('/readiness', tags=["Health Checks"], responses=responses_readiness,
            summary=descriptions['readiness'])
@autodynatrace.trace(f'{prefix}/readiness')
@tracer.wrap(service='basetemplate', resource=f'{prefix}/liveness')
def readiness() -> HttpResponse:
    return WorkerController.readiness()


@router.get('', tags=["HelloWorld"], responses=responses_hello_world,
            summary=descriptions['get_hello_world'])
@autodynatrace.trace(f'{prefix}')
@tracer.wrap(service='basetemplate', resource=f'{prefix}')
def hello_world(env: str = Header(
        default='', description="Ambiente a utilizar en el request")) -> HttpResponse:
    """ Responde con un 'Hello World'. """
    return WorkerController.hello_world(env)


@router.get('/person', tags=["HelloWorld"], responses=responses_hello_world,
            summary=descriptions['get_hello_person'])
@autodynatrace.trace(f'{prefix}/person')
@tracer.wrap(service='basetemplate', resource=f'{prefix}/person')
def hello_person(input: Person = Depends()) -> HttpResponse:
    """ input: Person = Depends() --> Recibe la entidad Person como Query Params. """
    return WorkerController.hello_world()


@router.post('/person/{id}', tags=["HelloWorld"], responses=responses_hello_world,
             summary=descriptions['post_hello_person'])
@autodynatrace.trace(f'{prefix}/person/<id>')
@tracer.wrap(service='basetemplate', resource=f'{prefix}/person/<id>')
def hello_person(id: int, input: Person) -> HttpResponse:
    """ id: int --> Recibe un id de tipo entero como Path Param.
        input: Person --> Recibe la entidad Person como Body. """
    return WorkerController.hello_world()
