from fastapi import FastAPI
from db import models
from db.database import engine
from src.routers import player, team

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(player.router)
app.include_router(team.router)
