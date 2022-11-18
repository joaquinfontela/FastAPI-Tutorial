from db import models
from typing import Union
from src.models.Team import Team


def convert_team_model_to_team(team_model: models.Team) -> Union[Team, None]:
    if not team_model:
        return None
    return Team(id=team_model.id, name=team_model.name,
                country=team_model.country, cur_pos_league=team_model.cur_pos_league)
