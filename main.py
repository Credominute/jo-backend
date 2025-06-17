import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.routing import APIRoute

# slowapi
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# API & DB
from api.order_api import OrderApi
from api.ticket_api import TicketApi
from api.user_api import UserApi
from api.auth import router as auth_router
from src.config.database import engine, Base
from src.config.rate_limiter import limiter

# Création des tables sans suppression des données existantes
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Limiteur de requêtes
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Gestion d’erreur du limitateur
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Trop de requêtes. Veuillez patienter."}
    )

# CORS (uniquement autorisé pour le front Netlify)
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
# Initialisation des APIs
user_api = UserApi()
ticket_api = TicketApi()
order_api = OrderApi()

app.include_router(user_api.router, prefix='/user', tags=["Users"])
app.include_router(order_api.router, prefix='/order', tags=["Order"])
app.include_router(ticket_api.router, prefix='/ticket', tags=["Tickets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


# Endpoints de test et de diagnostic
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

# Lancement local
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)