from pydantic import BaseModel, Field
from .general_schemas import (
    DataSchema,
    MetaSchema,
    error_response_general
)


class ReadinessSchema(BaseModel):
    """
        Readiness Schema
    """
    data: DataSchema = Field(
        default=DataSchema(status="Mongo is alive"),
        title="DataSchema"
    )
    meta: MetaSchema = Field(...)


responses_readiness = {
    200: {"model": ReadinessSchema},
    500: error_response_general
}
