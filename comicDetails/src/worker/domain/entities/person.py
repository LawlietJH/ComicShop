from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int
    status: Optional[bool] = True

    class Config:
        schema_extra = {
            'example': {
                'name': 'Juan',
                'age': 30,
                'status': True
            }
        }
