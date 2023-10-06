from pydantic import BaseModel, Field


class SingupSchema(BaseModel):
    """ Singup Schema """
    status: str = Field(
        default="Hello World",
        title="Status",
        description="Estatus del servicio"
    )


responses_singup = {
    200: {'model': SingupSchema},
    422: {}
}
