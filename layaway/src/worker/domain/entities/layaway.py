from pydantic import BaseModel


class Layaway(BaseModel):
    comic_id: int
