from pydantic import BaseModel, Field


class HelloWorldSchema(BaseModel):
    """
        Liveness Schema
    """
    status: str = Field(
        default="Hello World",
        title="Status",
        description="Estatus del servicio"
    )


responses_hello_world = {
    200: {"model": HelloWorldSchema}
}