from db import models
from src.models.Player import Player
from src.helpers.team_helper import convert_team_model_to_team


def convert_player_model_to_player(player_model: models.Player) -> Player:
    return Player(id=player_model.id, name=player_model.name, nationality=player_model.nationality,
                  age=player_model.age, field_pos=player_model.field_pos,
                  team=convert_team_model_to_team(player_model.team))
