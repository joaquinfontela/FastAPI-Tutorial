from fastapi import APIRouter, status, HTTPException
from typing import Dict, List, Optional
from src.helpers.team_helper import convert_team_model_to_team
from src.models.Team import BaseTeam, Team, TeamTemplate
from src.repositories.team_repository import TeamRepository, NoTeamException
import logging

router = APIRouter(
    prefix='/teams',
    tags=['teams']
)


@router.get("", response_model=Dict[str, List[Team]], status_code=status.HTTP_200_OK)
def get_teams(skip: int = 0, limit: Optional[int] = None):
    logging.debug(
        f'Searching teams with SKIP = {skip} and ' + 'NO LIMIT' if not limit else 'LIMIT = {limit}')
    teams = TeamRepository().get_teams(skip=skip, limit=limit)
    return {'teams': [convert_team_model_to_team(team) for team in teams]}


@router.get("/{id}", response_model=Team, status_code=status.HTTP_200_OK)
def get_team(id: int):
    logging.debug(
        f'Searching team with ID = {id}')
    try:
        return convert_team_model_to_team(TeamRepository().get_team(id))
    except NoTeamException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Team with id {id} not found.')


@router.post("", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team_data: BaseTeam):
    logging.debug(f'Creating team with data: {dict(team_data)}')
    new_team = TeamRepository().create_team(
        team_data.name, team_data.country, team_data.cur_pos_league)
    return Team(id=new_team.id, name=new_team.name, country=new_team.country,
                cur_pos_league=new_team.cur_pos_league)


@router.put('/{id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def update_team(id: int, team_data: TeamTemplate):
    logging.debug(f'Updating team with id: {id}, with data: {dict(team_data)}')
    try:
        updated_team = TeamRepository().update_team(id, team_data.name, team_data.country,
                                                    team_data.cur_pos_league)
        return convert_team_model_to_team(updated_team)
    except NoTeamException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Team with id {id} not found.')


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: int):
    logging.debug(f'Deleting team with id: {id}')
    try:
        TeamRepository().delete_team(id)
        return {'status': f'Team with id {id} deleted successfully.'}
    except NoTeamException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Team with id {id} not found.')
