from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    cur_pos_league = Column(Integer)

    players = relationship("Player", back_populates='team')


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    nationality = Column(String)
    age = Column(Integer)
    field_pos = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete='SET NULL'))

    team = relationship("Team", back_populates='players')
