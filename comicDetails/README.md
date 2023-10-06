# Introducción

Plantilla para servicios Rest usando FastApi y Arquitectura hexagonal con Python 3.11.0 o superior.

# Estructura

    .
    ├── config_mongodb          # Archivos de configuración de base de datos
    ├── docs                    # Archivos esperados de base de datos
    ├── src                     # Archivos de la aplicación
    │    ├── shared             # Clases compartidas para las diferentes capas del servicio
    │    │  ├── domain          # Capa de dominio para shared
    │    │  └── infrastructure  # Capa de infraestructura para shared
    │    │      └── logs        # Clases y configuraciones para logs
    │    └── worker             # Código funcional del microservicio
    │       ├── application     # Capa de aplicación para el worker
    │       ├── domain          # Capa de dominio para worker
    │       └── infrastructure  # Capa de infraestructura para worker
    └── tests                   # Tests del servicio
        ├── integration_tests   # Contiene los tests de integración del worker
        │   ├── application
        │   ├── domain
        │   └── infrastructure
        └── unit_tests          # Contiene los tests unitarios del worker
            ├── application
            ├── domain
            ├── infrastructure
            └── mock_data       # Respuestas esperadas por servicios externos en formato json

### Capas de la arquitectura hexagonal

1. domain: contiene el núcleo de la aplicación, es decir, las entidades y los repositorios. Esta capa es independiente
   del framework y se puede reutilizar en diferentes plataformas.
2. application: contiene el código relacionado con la interfaz de la aplicación, es decir, los casos de uso y los
   servicios que se comunican con el núcleo de la aplicación
3. infrastructure: contiene el código relacionado con la infraestructura de la aplicación, como los repositorios, las
   rutas de FastApi y los controladores.

# Cómo empezar

1. Contar con la versión de python 3.11.0 o superior. Es importante el uso de un ambiente virtual como pyenv o virtualenv 
   en que se deberán instalar las dependencias en el siguiente paso.
2. Instalar las dependencias necesarias para el funcionamiento del servicio.

Archivo: **requirements.txt**
```bash
aiohttp==3.8.4
autodynatrace==2.0.0
coverage==7.2.7
dependency-injector==4.41.0
fastapi==0.99.0
fire==0.5.0
firebase-admin==6.2.0
httpx==0.24.1
log4python==1.0.3
pydantic==1.10.12
pymongo==4.4.0
pytest==7.4.0
pytest-env==0.8.2
pytest-mock==3.11.1
redis==4.6.0
uvicorn==0.22.0
ddtrace==1.20.0
```

```bash
pip install -r requirements.txt
```

3. Configurar las variables de entorno necesarias, aquí un ejemplo de ellas (solo utilizar las necesarias para el servicio):

Archivo: **.env.sample**
```bash
# APP:
export APP_NAME=ComicShop
export SERVICE_NAME=comicDetails
export NAMESPACE=catalogs
export API_VERSION=v1
export RESOURCE=comics
export IMAGE_VERSION=1.0.0
export ENABLE_DOCS=true
export PORT=8001
export RELOAD=true

# MONGO:
export MONGO_DB_NAME=users
export MONGO_TIMEOUT_MS=500
export MONGO_MAX_POOL_SIZE=20
export MONGO_ID_ERROR_DETAILS=errorDetails

# REDIS:
export REDIS_EXPIRATION_MINS=1440

# FIREBASE:
export FIREBASE_KEY_PATH=
export FIREBASE_DEFAULT_DB=
export FIREBASE_TIMEOUT_SEC=5

# LOGS:
export VERSION_LOG=v1
export APPENDERS=console

# OTROS:
export DEVELOPER_PORTAL_HTTP_ERRORS=
export HTTP_TIMEOUT_SEC=15
export STORE_ID=10151
```

Para agregar las variables de entorno a la sesión actual en la terminal (No tienen persistencia):
```bash
source .env.sample
```

Descripciones:

-APP:
* ***APP_NAME**: Nombre de la aplicación. Utilizado en los logs.
* ***SERVICE_NAME**: Nombre del servicio.
* ***NAMESPACE**: Namespace utilizado para las rutas.
* ***API_VERSION**: Versión de la API utilizada para las rutas.
* ***RESOURCE**: Nombre del recurso en el endpoint.
* ***IMAGE_VERSION**: Versión de la imagen, utilizado para la documentación en Swagger.
* **ENABLE_DOCS**: Permite habilitar o deshabilitar la documentación de swagger. Default: False.
* **PORT**: Se utiliza para indicar un puerto distinto en local. Default: 8000.
* **RELOAD**: Indíca si se desea actualizar la aplicación en automático cuando se modifica el código. Default: False.

-Mongo:
* ***MONGO_DB_NAME**: Nombre de la base de datos de configuraciones.
* ***MONGO_TIMEOUT_MS**: Indica un tiempo de timeout en milisegundos.
* ***MONGO_MAX_POOL_SIZE**: Indica el tamaño máximo de conexiones disponibles.
* **MONGO_ID_GLOBAL_CONFIG**: ID del documento de configuraciones globales en Mongo.
* ***MONGO_ID_GENERAL_CONFIG**: ID del documento de configuraciones generales en Mongo.
* ***MONGO_ID_ERROR_DETAILS**: ID del documento de errores en Mongo.
* **MONGO_ID_SERVICE_CONFIG**: ID del documento de configuraciones propias del servicio en Mongo.

-Redis: Si fuera necesario.
* ***REDIS_EXPIRATION_MINS**: Indica en minutos el tiempo de expiración asignado a una key en Redis.

-Firebase: Si fuera necesario.
* ***FIREBASE_KEY_PATH**: Ruta del archivo de credenciales `firebase.json`.
* ***FIREBASE_TIMEOUT_SEC**: Timeout en segundos para peticiones a Firebase.
* ***FIREBASE_DEFAULT_DB**: URL de firebase base para peticiones.

-Requests: Si fuera necesario.
* ***HTTP_TIMEOUT_SEC**: Timeout en segundos para peticiones request.

-Logs:
* ***VERSION_LOG**=v1
* ***APPENDERS**: Parámetro de salida de los logs, puede ser `file` o `console`, los cuales mandarian los logs a `src/service.log` o a la terminal respectivamente. 

-Otros:
* ***DEVELOPER_PORTAL_HTTP_ERRORS**=URL del developer portal en su sección /errors.
* **STORE_ID**=10151

Nota: Solo agregar los de redis o firebase si estos son necesarios. Los que tienen un asterisco son obligatorios.

4. Mandar los `logs` a un archivo en ambiente local

Para lograr que se manden los logs a un archivo al lado de `main.py` de nuestro proyecto, hay que agregar en los `appenders` del archivo `log4p.py`, el diccionario `file` con lo siguiente:
```python
   ...
   'appenders': {
      'file': {
         'type': 'file',
         'FileName': 'service.log',  # log file name
         'backup_count': 5,  # files count use backup log
         'file_size_limit': 1024 * 1024 * 500,  # single log file size, default :20MB
         'PatternLayout': "%(message)s"
      },
      'console': {
         ...
```

Además habrá que cambiar la variable de entorno `APPENDERS=file` para que se envíen los logs al archivo con el nombre `service.log` en la carpeta `src/`.

5. Levantar el servicio

Ejecutar el archivo main:
```
python src/main.py
```

# Tests

Para correr los tests, solo será necesario ejecutar el siguiente comando dentro de la raíz de nuestro proyecto:

```bash
pytest tests/
```

Es importante mencionar que es necesario agregar tantos archivos de clases de tests como archivos se contengan en cada
una de las capas, y dentro de cada clase se debe probar cada función.

## Coverage

Para generar un archivo coverage hay que utilizar los siguientes comandos:

```bash
coverage run -m pytest tests/unit_tests/
coverage xml
```

Nota: Esto nos generaría un coverage solo de la carpeta unit_tests/.

## Sonar Scanner

Para poder hacer un análisis de cobertura en un proyecto de SonarQube es necesario agregar un archivo de configuración llamado `sonar-project.properties`.

Archivo: **sonar-project.properties**
```
sonar.projectKey=comicDetails
sonar.host.url=http://localhost:9000
sonar.token=sqp_0123456789abcdef0123456789abcdef01234567
sonar.sources=src/worker
sonar.tests=tests/
sonar.sourceEncoding=UTF-8
sonar.python.file.suffixes=py
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.version=3
sonar.coverage.exclusions=src/worker/infrastructure/worker_routes.py,src/worker/infrastructure/worker_controller.py
```

Los campos `sonar.projectKey` y `sonar.token` deben cambiarse por los datos propios del proyecto en SonarQube.

Con este archivo creado, podemos ejecutar la tarea en SonarQube con el comando:
```bash
sonar-scanner
```

# Logs

La clase Log cuenta con el atributo 'measurement', con el propósito de obtener métricas específicas para cada
transacción dentro del microservicio. Dicho atributo es del tipo 'Measurement' y se encuentra en la ruta:

```bash
src/shared/infrastructure/logs/measurement.py
```

La clase cuenta con los atributos:

- service: string con el servicio consultado
- message: mensaje con el detalle de la transacción
- time_elapsed: tiempo de ejecución en milisegundos

A continuación se presenta un ejemplo de log sin métricas (nótese el atributo al final de la cadena):

```bash
{"level": "INFO", "log_origin": "INTERNAL", "timestamp": "2023-01-31 13:51:35.614923", "tracing_id": "914befc8-cba3-4413-b8ee-12b678928f9a", "hostname": "250520M90280185.local", "service": "landingpages", "appname": "LandingPages", "total_time": 43, "message": "Mongo is alive"}
```

En seguida, un ejemplo de log con métricas (nótese el atributo al final de la cadena):

```bash
{"level": "INFO", "log_origin": "INTERNAL", "timestamp": "2023-01-31 13:51:35.614393", "tracing_id": "914befc8-cba3-4413-b8ee-12b678928f9a", "hostname": "250520M90280185.local", "service": "landingpages", "appname": "LandingPages", "total_time": 42, "message": "Mongo is alive", "measurement": {"service": "MongoDB", "message": "Success", "time_elapsed": 41.98}}
```

A continuación, un ejemplo de implementación:

```python
self._log.error(
   "Error al obtener configuraciones de MongoDB.",
   method=Utils.get_method_name(self, 'execute'),
   error="Ha ocurrido un error al obtener las configuraciones",
   measurement=Measurement('MongoDB', time_elapsed, 'Error'))
```

# Para tomar en cuenta

A lo largo de toda la plantilla se encontrarán comentarios de ayuda, explicaciones o ejemplos que deberán eliminarse
durante la fase de desarrollo, así como los "TODO" que se encuentren en ella.

También deberá editarse este archivo README con la información actualizada del microservicio desarrollado.
