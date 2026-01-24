from pydantic import BaseModel


class DepartementData(BaseModel):
    number: str
    name: str