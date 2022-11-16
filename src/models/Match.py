from pydantic import BaseModel


class Match(BaseModel):
    id: int
    home_team: str
    away_team: str
    year: int
    round: str
    home_score: int
    away_score: int
