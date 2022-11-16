from typing import Optional
from pydantic import BaseModel


class BasePlayer(BaseModel):
    name: str
    nationality: str
    age: int
    club: Optional[str] = None
    field_pos: str


class Player(BasePlayer):
    id: int
