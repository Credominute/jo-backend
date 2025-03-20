from fastapi import FastAPI

from api.api import UserApi, TicketApi, OrderApi
from api.auth import router as auth_router
from src.config.database import engine, Base

# Création des tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

#Initialisation des api User, Ticket et Order
user_api = UserApi()
ticket_api = TicketApi()
order_api = OrderApi()

# Montage des routes de JO24API
app.include_router(user_api.router, prefix='/user', tags=["Users"])
app.include_router(user_api.router, prefix='/order', tags=["Order"])
app.include_router(user_api.router, prefix='/ticket', tags=["Tickets"])

app.include_router(auth_router, prefix="/auth", tags=["Auth"])