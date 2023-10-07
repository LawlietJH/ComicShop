from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, schema, validator
from pydantic.fields import ModelField


class User(BaseModel):
    id: str
    username: str
