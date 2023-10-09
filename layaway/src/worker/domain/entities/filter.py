from typing import Optional

from pydantic import BaseModel


class Filter(BaseModel):
    order_by: Optional[str] = 'id'
    reverse: Optional[bool] = False
