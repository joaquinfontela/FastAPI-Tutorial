from typing import Optional, Union
from pydantic import BaseModel
from src.models.Team import Team


class PlayerTemplate(BaseModel):
    name: str
    nationality: str
    age: int
    field_pos: str
    team_id: Optional[int] = ...


class BasePlayer(BaseModel):
    name: str
    nationality: str
    age: int
    field_pos: str
    team: Optional[Team]


class Player(BasePlayer):
    id: int
