from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi

from api.auth import router as auth_router
from src.config.database import engine, Base

""" Création des tables : utilisation d'une fonction :
    On supprime/recrée la base de données pour les tests
def drop_and_create_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) """

# Création des tables sans suppression des données existantes
Base.metadata.create_all(bind=engine)

""" Exécution de la suppression/recréation de la base au démarrage : 
    contenu déprécié pour référence puis actuel recommandé/lifespan
@app.on_event("startup")
def startup_event():
    drop_and_create_database()
@asynccontextmanager
async def lifespan(app: FastAPI):
    drop_and_create_database()
    yield
    
# Création de l'application FastAPI avec lifespan
app = FastAPI(lifespan=lifespan)"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test_CORS sans passer par l'authentification (route : /ping)
@app.get("/ping")
def ping():
    return {"message": "pong"}

# Initialisation des api User, Ticket et Order
user_api = UserApi()
ticket_api = TicketApi()
order_api = OrderApi()

# Montage des routes de JO24API
app.include_router(user_api.router, prefix='/user', tags=["Users"])
app.include_router(order_api.router, prefix='/order', tags=["Order"])
app.include_router(ticket_api.router, prefix='/ticket', tags=["Tickets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
