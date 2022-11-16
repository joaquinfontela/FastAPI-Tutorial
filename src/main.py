from fastapi import FastAPI, status, HTTPException
from typing import Dict, List, Union
from db import models
from db.database import engine
from src.helpers.team_helper import convert_team_model_to_team
from src.repositories.player_repository import PlayerRepository
from src.repositories.team_repository import TeamRepository, NoTeamException
from src.models.Player import BasePlayer, Player
from src.models.Team import BaseTeam, Team, TeamTemplate
import logging

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/players", response_model=Dict[str, List[Player]], status_code=status.HTTP_200_OK, deprecated=True)
def get_players(skip: int = 0, limit: Union[int, None] = None):
    logging.debug(
        f'Searching players with SKIP = {skip} and ' + 'NO LIMIT' if not limit else 'LIMIT = {limit}')
    return PlayerRepository().get_players(skip=skip, limit=limit)


@app.get("/teams", response_model=Dict[str, List[Team]], status_code=status.HTTP_200_OK)
def get_teams(skip: int = 0, limit: Union[int, None] = None):
    logging.debug(
        f'Searching teams with SKIP = {skip} and ' + 'NO LIMIT' if not limit else 'LIMIT = {limit}')
    teams = TeamRepository().get_teams(skip=skip, limit=limit)
    return {'teams': [convert_team_model_to_team(team) for team in teams]}


@app.get("/teams/{id}", response_model=Team, status_code=status.HTTP_200_OK)
def get_team(id: int):
    logging.debug(
        f'Searching team with ID = {id}')
    try:
        return convert_team_model_to_team(TeamRepository().get_team(id))
    except NoTeamException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Team with id {id} not found.')


@app.post("/players", response_model=Player, status_code=status.HTTP_201_CREATED, deprecated=True)
def create_player(player_data: BasePlayer):
    logging.debug(f'Creating player with data: {dict(player_data)}')
    res = PlayerRepository().create_player(
        player_data.name, player_data.nationality, player_data.age,
        player_data.club, player_data.field_pos)
    return Player(**res)


@app.post("/teams", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team_data: BaseTeam):
    logging.debug(f'Creating team with data: {dict(team_data)}')
    new_team = TeamRepository().create_team(
        team_data.name, team_data.country, team_data.cur_pos_league)
    return Team(id=new_team.id, name=new_team.name, country=new_team.country,
                cur_pos_league=new_team.cur_pos_league)


@app.put('/teams/{id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def update_team(id: int, team_data: TeamTemplate):
    logging.debug(f'Updating team with id: {id}, with data: {dict(team_data)}')
    try:
        updated_team = TeamRepository().update_team(id, team_data.name, team_data.country,
                                                    team_data.cur_pos_league)
        return convert_team_model_to_team(updated_team)
    except NoTeamException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Team with id {id} not found.')


@app.delete('/teams/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: int):
    logging.debug(f'Deleting team with id: {id}')
    try:
        TeamRepository().delete_team(id)
        return {'status': f'Team with id {id} deleted successfully.'}
    except NoTeamException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Team with id {id} not found.')
