from pydantic import BaseModel, Field


class LayawaySchema(BaseModel):
    """ Layaway Schema """
    status: str = Field(
        default="Hello World",
        title="Status",
        description="Estatus del servicio"
    )


responses_layaway = {
    200: {'model': LayawaySchema},
    422: {}
}
