from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Dict, List, Optional
from src.helpers.player_helper import convert_player_model_to_player
from src.models.Player import Player, PlayerTemplate
from src.repositories.player_repository import PlayerRepository
from src.repositories.team_repository import NoTeamException
import logging

router = APIRouter(
    prefix='/players',
    tags=['players']
)


@router.get("", response_model=Dict[str, List[Player]], status_code=status.HTTP_200_OK)
def get_players(skip: int = 0, limit: Optional[int] = None):
    logging.debug(
        f'Searching players with SKIP = {skip} and ' + 'NO LIMIT' if not limit else 'LIMIT = {limit}')
    players = PlayerRepository().get_players(skip=skip, limit=limit)
    return {'players': [convert_player_model_to_player(player) for player in players]}


@router.post("", response_model=Player, status_code=status.HTTP_201_CREATED)
def create_player(player_data: PlayerTemplate):
    print(f'Creating player with data: {dict(player_data)}')
    try:
        new_player = PlayerRepository().create_player(
            player_data.name, player_data.nationality, player_data.age,
            player_data.field_pos, player_data.team_id)
    except NoTeamException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'Team with id {player_data.team_id} does not exist.')
    return Player(id=new_player.id, name=new_player.name, nationality=new_player.nationality,
                  age=new_player.age, field_pos=new_player.field_pos,
                  team=jsonable_encoder(new_player.team)
                  )
