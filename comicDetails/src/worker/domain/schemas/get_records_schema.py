from pydantic import BaseModel, Field


class RecordsSchema(BaseModel):
    """ Records Schema """
    status: str = Field(
        default="Hello World",
        title="Status",
        description="Estatus del servicio"
    )


responses_get_records = {
    200: {'model': RecordsSchema},
    422: {}
}
