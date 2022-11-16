from pydantic import BaseModel
from typing import Optional


class BaseTeam(BaseModel):
    name: str
    country: str
    cur_pos_league: int


class TeamTemplate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    cur_pos_league: Optional[int] = None


class Team(BaseTeam):
    id: int
