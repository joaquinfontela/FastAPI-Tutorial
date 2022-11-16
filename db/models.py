from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    cur_pos_league = Column(Integer)


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    nationality = Column(String)
    age = Column(Integer)
    field_pos = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
