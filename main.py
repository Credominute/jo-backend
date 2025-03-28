from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi

from api.auth import router as auth_router
from src.config.database import engine, Base

# Création des tables : utilisation d'une fonction
def drop_and_create_database():
    """Supprime et recrée la base de données en environnement de test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Exécution de la suppression/recréation de la base au démarrage (test)
@app.on_event("startup")
def startup_event():
    drop_and_create_database()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=[""]
)

#Initialisation des api User, Ticket et Order
user_api = UserApi()
ticket_api = TicketApi()
order_api = OrderApi()

# Montage des routes de JO24API
app.include_router(user_api.router, prefix='/user', tags=["Users"])
app.include_router(user_api.router, prefix='/order', tags=["Order"])
app.include_router(user_api.router, prefix='/ticket', tags=["Tickets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
