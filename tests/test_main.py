"""
Tests principaux pour l'application FastAPI.

- `test_ping()`: Vérifie que l'API répond correctement sur `/ping`.
- `test_cors_headers()`: Vérifie que les en-têtes CORS sont bien présents.
- `test_redirect_to_docs()`: Vérifie que `/api` redirige bien vers la documentation.
- `test_user_endpoint()`: Vérifie que l'endpoint `/user` est accessible et renvoie du JSON.
- `test_order_endpoint()`: Vérifie que l'endpoint `/order` est accessible et renvoie du JSON.
- `test_ticket_endpoint()`: Vérifie que l'endpoint `/ticket` est accessible et renvoie du JSON.

⚠️ Pour les tests en environnement de test, la base de données peut être réinitialisée
via `drop_and_create_database()`. Cette fonction **n'est pas utilisée** dans `main.py`
en production, mais peut être activée en cas de besoin. La fonction de réinitialisation
de la base de données (à utiliser uniquement pour les tests) est (avec lifespan) :

def drop_and_create_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    drop_and_create_database()
    yield
app = FastAPI(lifespan=lifespan)
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# test de santé (on vérifie que l'API répond)
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

# test_CORS (les en-têtes CORS sont bien présents)
def test_cors_headers():
    response = client.get("/ping")
    assert response.headers.get("access-control-allow-origin") == "*"

# test de redirection vers Swagger (pour l'administrateur)
def test_redirect_to_docs():
    response = client.get("/api", follow_redirects=False)
    assert response.status_code == 307  # Redirection temporaire
    assert response.headers["location"] == "/docs"

# Ou bien via des tests automatiques des endpoints
def test_user_endpoint():
    response = client.get("/user")
    assert response.status_code == 200  # Vérifie que l'API répond
    assert "application/json" in response.headers["content-type"]  # Vérifie le type de contenu

def test_order_endpoint():
    response = client.get("/order")
    assert response.status_code == 200  # Vérifie que l'API répond
    assert "application/json" in response.headers["content-type"]  # Vérifie le type de contenu

def test_ticket_endpoint():
    response = client.get("/ticket")
    assert response.status_code == 200  # Vérifie que l'API répond
    assert "application/json" in response.headers["content-type"]  # Vérifie le type de contenu