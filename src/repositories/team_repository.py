from typing import Dict, List, Union
from db.database import SessionLocal
from db import models
import logging


class NoTeamException(Exception):
    pass


class TeamRepository:

    def __init__(self):
        self.db = SessionLocal()

    def create_team(self, name: str, country: str, cur_pos_league: str) -> models.Team:
        new_team = models.Team(name=name, country=country,
                               cur_pos_league=cur_pos_league)
        self.db.add(new_team)
        self.db.commit()
        self.db.refresh(new_team)
        return new_team

    def delete_team(self, id: int):
        team = self.db.query(models.Team).filter(
            models.Team.id == id).delete(synchronize_session=False)
        self.db.commit()
        logging.debug('TEAMS FOUND: ',  team)
        if not team:
            raise NoTeamException()
        return team

    def get_teams(self, skip: int, limit: Union[int, None] = None) -> List[models.Team]:
        teams = self.db.query(models.Team).offset(skip).limit(limit)
        return teams

    def get_team(self, id: int):
        team = self.db.query(models.Team).filter(models.Team.id == id).first()
        if not team:
            raise NoTeamException()
        return team

    def update_team(self, id: int, name: str, country: str, cur_pos_league: str):
        team = self.db.query(models.Team)\
            .filter(models.Team.id == id)\
            .update({models.Team.name: name if name else models.Team.name,
                    models.Team.country: country if country else models.Team.country,
                    models.Team.cur_pos_league: cur_pos_league if cur_pos_league else models.Team.cur_pos_league},
                    synchronize_session=False)
        self.db.commit()
        logging.debug('TEAMS FOUND: ',  team)
        if not team:
            raise NoTeamException()
        return self.db.query(models.Team).filter(models.Team.id == id).first()
