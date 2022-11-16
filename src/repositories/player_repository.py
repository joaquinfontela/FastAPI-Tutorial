from typing import Dict, List, Union
from fastapi.encoders import jsonable_encoder
from db.database import SessionLocal
from db import models
import json
import logging


class PlayerRepository:

    def get_players(self, skip: int, limit: Union[int, None] = None) -> Dict[str, List]:
        return
        db = SessionLocal()
        players = db.query(models.Player).all()
        return players

    def create_player(self, name: str, nationality: str, age: int, club: str, field_pos: str):
        return
        with open('db/players.json', 'r') as players_file:
            players_data = json.loads(players_file.read())
        max_id = players_data['max_id']

        player_data_with_id = {'name': name, 'nationality': nationality,
                               'age': age, 'club': club, 'field_pos': field_pos, 'id': str(max_id + 1)}
        logging.debug(f'CURRENT MAX_ID = {str(max_id + 1)}')

        players_data['players'].append(jsonable_encoder(player_data_with_id))
        players_data['max_id'] = max_id + 1

        with open('db/players.json', 'w') as players_file:
            players_file.write(json.dumps(players_data))

        return player_data_with_id
