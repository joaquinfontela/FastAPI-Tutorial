from typing import List, Optional, Union
from fastapi.encoders import jsonable_encoder
from db.database import SessionLocal
from db import models
from src.repositories.team_repository import NoTeamException
import logging


class PlayerRepository:

    def __init__(self):
        self.db = SessionLocal()

    def get_players(self, skip: int, limit: Optional[int] = None) -> List[models.Player]:
        players = self.db.query(models.Player).offset(skip).limit(limit)
        return players

    def create_player(self, name: str, nationality: str, age: int,
                      field_pos: str, team_id: Union[int, None]) -> models.Player:
        logging.debug("TEAM_ID: ", team_id)
        if team_id and not self.db.query(models.Team).filter(
                models.Team.id == team_id).first():
            raise NoTeamException()
        new_player = models.Player(name=name, nationality=nationality, age=age,
                                   field_pos=field_pos, team_id=team_id)
        self.db.add(new_player)
        self.db.commit()
        self.db.refresh(new_player)
        return new_player
