# layaway

**Sistema de apartado de cómics.**

    Creado con FastAPI y Arquitectura Hexagonal.
    Python: 3.11.0

Es posible ver la documentación en: **/orders/api/v1/layaway/docs**

## Endpoints

* **/orders/api/v1/layaway**
    * **GET:** Obtiene el listado de apartados de un usuario.
    * **POST:** Agrega un Cómic al sistema de apartados de un usuario.

## Ejecución

```bash
python src/main.py
```

### Pruebas Unitarias

```bash
pytest tests/unit_tests/
```

### Pruebas de Integración

```bash
pytest tests/integration_tests/
```

## Dependencias:

Instalación:

```bash
pip install -r requirements.txt
```

Archivo: **requirements.txt**

```bash
aiohttp==3.8.4
autodynatrace==2.0.0
coverage==7.2.7
ddtrace==1.20.1
dependency-injector==4.41.0
fastapi==0.99.0
fire==0.5.0
firebase-admin==6.2.0
httpx==0.24.1
log4python==1.0.3
pymongo==4.4.0
pytest==7.4.0
pytest-env==0.8.2
pytest-mock==3.11.1
redis==4.6.0
uvicorn==0.22.0
```

## Variables De Entorno

Comando:

```bash
source .env.sample
```

Script .env.sample:
```bash
# APP:
export APP_NAME=ComicShop
export SERVICE_NAME=Layaway
export NAMESPACE=orders
export API_VERSION=v1
export RESOURCE=layaway
export IMAGE_VERSION=1.0.0
export ENABLE_DOCS=true
export PORT=8002
export RELOAD=true

# MONGO:
export MONGO_DB_NAME=configs
export MONGO_DB_NAME_ORDERS=orders
export MONGO_TIMEOUT_MS=500
export MONGO_MAX_POOL_SIZE=20
export MONGO_ID_ERROR_DETAILS=errorDetails

# LOGS:
export VERSION_LOG=v1
export APPENDERS=console

# OTROS:
export URL_VALIDATE_TOKEN=
export URL_RECORDS=
export DEVELOPER_PORTAL_HTTP_ERRORS=
export HTTP_TIMEOUT_SEC=15
```


## Configuración para SonarQube en local

Archivo: **sonar-project.properties**

```bash
sonar.projectKey=layaway
sonar.host.url=http://localhost:9000
sonar.token=
sonar.sources=src/worker
sonar.tests=tests/
sonar.sourceEncoding=UTF-8
sonar.python.file.suffixes=py
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.version=3
sonar.coverage.exclusions=src/worker/infrastructure/worker_routes.py,src/worker/infrastructure/worker_controller.py
```

### Coverage

Coverage Run: `coverage run -m pytest tests/unit_tests`
Coverage Xml: `coverage xml`
Sonar Scanner: `sonar-scanner`
