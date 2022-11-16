from db import models
from src.models.Team import Team


def convert_team_model_to_team(team_model: models.Team) -> Team:
    return Team(id=team_model.id, name=team_model.name,
                country=team_model.country, cur_pos_league=team_model.cur_pos_league)
