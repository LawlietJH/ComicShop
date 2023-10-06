from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseModel, Field
from pydantic.schema import schema

from shared.infrastructure.settings import get_settings

settings = get_settings()
developer_portal_errors_url = settings.DEVELOPER_PORTAL_HTTP_ERRORS


class DataSchema(BaseModel):
    """
        Data Schema
    """
    status: str = Field(
        title="Status",
        description="Estatus de los servicios utilizados"
    )


class ErrorDataSchema(BaseModel):
    """
        Error Data Schema
    """
    user_message: str = Field(
        title="User Message",
        description="Mensaje de error para el usuario"
    )


class MetaSchema(BaseModel):
    """
        Meta Schema
    """
    time_elapsed: float = Field(
        default=1.0,
        title="Time elapsed",
        description="Tiempo de ejecución la operación"
    )
    timestamp: str = Field(
        default="2023-02-24T09:09:39.196026",
        title="Timestamp",
        description="Fecha en formato UTC"
    )
    transaction_id: str = Field(
        default="b284993c-323b-455a-87b9-ebf70b62bfa2",
        title="Transaction ID",
        description="Identificador único de la operación"
    )


class ErrorMetaSchema(BaseModel):
    """
        Error Meta Schema
    """
    error_code: int = Field(
        title="Error Code",
        description="Identificador único del error"
    )
    info: str = Field(
        title="Info",
        description="URL donde se encuentra información detallada del error"
    )
    timestamp: str = Field(
        default="2023-02-24T09:09:39.196026",
        title="Timestamp",
        description="Fecha en formato UTC"
    )
    transaction_id: str = Field(
        default="b284993c-323b-455a-87b9-ebf70b62bfa2",
        title="Transaction ID",
        description="Identificador único de la operación"
    )


class ErrorGeneralSchema(BaseModel):
    """
        Error General Schema
    """
    data: ErrorDataSchema = Field(...)
    meta: ErrorMetaSchema = Field(...)


error_general_schema = schema([ErrorGeneralSchema], ref_prefix=REF_PREFIX)

error_response_general = {
    "description": "Internal Server Error",
    "content": {
        "application/json": {
            "schema": error_general_schema["definitions"][
                "ErrorGeneralSchema"],
            "examples": {
                "ErrorReadinessMongo": {
                    "value": ErrorGeneralSchema(
                        data=ErrorDataSchema(
                            user_message="Error de conexión a mongo."),
                        meta=ErrorMetaSchema(
                            error_code=100,
                            info=f"{developer_portal_errors_url}#500.General-Error.100"
                        )
                    )
                }
            }
        }
    }
}
