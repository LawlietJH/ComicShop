from typing import Optional

from pydantic import BaseModel


class Filter(BaseModel):
    name: Optional[str]
    page: Optional[int]
