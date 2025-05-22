import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi
from api.auth import router as auth_router
from src.config.database import engine, Base
from fastapi.routing import APIRoute

# Création des tables sans suppression des données existantes
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://capable-halva-2ecf91.netlify.app",
]
# Initialisation de CORS
app.add_middleware( # type: ignore
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/")
def root():
    return {"message": "API JO backend - disponible"}

@app.get("/api")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/test-cors")
def test_cors():
    return {"message": "CORS test passed"}

@app.get("/routes")
def list_routes():
    return [
        {
            "path": route.path,
            "methods": list(route.methods),
            "name": route.name
        }
        for route in app.routes
        if isinstance(route, APIRoute)
    ]

# Point d'entrée pour initialiser un serveur local
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)