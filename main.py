from fastapi import FastAPI

from api.api import UserApi
from src.config.database import engine, Base

# Création des tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

#Initialisation de l'api User
user_api = UserApi()

app.include_router(user_api.router,
                   prefix='/user',
                   tags=["Users"])
