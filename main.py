from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi

from api.auth import router as auth_router
from src.config.database import engine, Base

# Création des tables sans suppression des données existantes
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialisation de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des api User, Ticket et Order
user_api = UserApi()
ticket_api = TicketApi()
order_api = OrderApi()

# Montage des routes de JO24API
app.include_router(user_api.router, prefix='/user', tags=["Users"])
app.include_router(order_api.router, prefix='/order', tags=["Order"])
app.include_router(ticket_api.router, prefix='/ticket', tags=["Tickets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
