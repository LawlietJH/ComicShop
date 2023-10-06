from pydantic import BaseModel, Field


class HelloWorldSchema(BaseModel):
    """ Liveness Schema """
    status: str = Field(
        default="Hello World",
        title="Status",
        description="Estatus del servicio"
    )


responses_get_comics = {
    200: {'model': HelloWorldSchema},
    422: {}
}
