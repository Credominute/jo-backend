import os

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi
from api.auth import router as auth_router
from src.config.database import engine, Base


# Création des tables sans suppression des données existantes
# Base.metadata.create_all(bind=engine)

def drop_and_create_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    drop_and_create_database()
    yield
app = FastAPI(lifespan=lifespan)

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

# Pour les tests :
@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/api")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/test-cors")
def test_cors():
    return {"message": "CORS test passed"}

# Point d'entrée pour initialiser un serveur local
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)