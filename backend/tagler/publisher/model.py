from pydantic import BaseModel
class SQL_PUSH(BaseModel):
    id: int
    tag: str
    heal: str