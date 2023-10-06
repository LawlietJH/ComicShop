from typing import Optional

from pydantic import BaseModel


class Filter(BaseModel):
    contains: Optional[str]
    page: Optional[int]
    comic: Optional[str]
    character: Optional[str]
