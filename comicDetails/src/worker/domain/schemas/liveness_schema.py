from pydantic import BaseModel, Field


class LivenessSchema(BaseModel):
    """
        Liveness Schema
    """
    status: str = Field(
        default="success",
        title="Status",
        description="Estatus del servicio"
    )


responses_liveness = {
    200: {"model": LivenessSchema}
}
