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

# test de redirection vers Swagger (pour l'administrateur)
def test_redirect_to_docs():
    response = client.get("/api", follow_redirects=False)
    assert response.status_code == 307  # Redirection temporaire
    assert response.headers["location"] == "/docs"

# Ou bien via des tests automatiques des endpoints :

def test_user_endpoint():
    # 1. Création d'un utilisateur
    credentials = {
        "nom": "Test",
        "prenom": "User",
        "mail": "test@example.com",
        "telephone": "1234567890",
        "mot_de_passe": "testpassword"
    }
    response = client.post("/user/", json=credentials)
    print("Réponse de /user/:", response.status_code, response.json())
    # Vérification que l'utilisateur a bien été créé
    assert response.status_code == 200, f"Erreur: {response.json()}"

    # Vérification du contenu de la réponse
    user_data = response.json()
    assert "user_id" in user_data, "L'ID de l'utilisateur n'est pas présent dans la réponse"

    # 2. Authentification pour obtenir un token
    login_response = client.post("/auth/", json={
        "mail": "test@example.com",  # Utilisation de l'email pour l'authentification
        "mot_de_passe": "testpassword"
    })
    print("Réponse de /auth/:", login_response.status_code, login_response.json())

    # Vérification que la réponse d'authentification est correcte
    assert login_response.status_code == 200, f"Erreur: {login_response.json()}"
    token = login_response.json().get("access_token")
    assert token is not None, "Le jeton d'accès est manquant"

    # 3. Accès à la route protégée /user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user", headers=headers)
    print("Réponse de /user (protégée):", response.status_code, response.json())

    # Vérification de la réponse pour la route protégée
    assert response.status_code == 200, f"Erreur: {response.json()}"
    assert "application/json" in response.headers["content-type"]
    assert "user_id" in response.json(), "L'ID de l'utilisateur n'est pas présent dans la réponse"

# Test de création + récupération d'une commande
def test_create_and_get_order():
    # Étape 1 : Création d'une commande
    order_data = {
        "user_id": 1,
        "price": 100.0,
        "ticket_type": "single"
    }
    create_response = client.post("/order/", json=order_data)
    assert create_response.status_code in [200, 201], f"Erreur: {create_response.json()}"

    created_order = create_response.json()
    order_id = created_order.get("order_id")
    assert order_id, "order_id est absent de la réponse"

    # Étape 2 : Vérifier si ticket_type est bien retourné
    assert created_order.get("ticket_type") == "single", f"ticket_type absent: {created_order}"

    # Étape 3 : Récupération de la commande
    get_response = client.get(f"/order/{order_id}")
    assert get_response.status_code == 200, f"Erreur récupération: {get_response.json()}"
    retrieved_order = get_response.json()

    # Vérifier que l'ordre récupéré contient bien les bonnes données
    assert retrieved_order.get("ticket_type") == "single", f"ticket_type incorrect: {retrieved_order}"

# Test de récupération des tickets
def test_ticket_endpoint():
    response = client.get("/ticket")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

# Test de création d'un ticket lié à une commande
def test_create_ticket():
    # Étape 1 : Créer une commande pour attacher un ticket
    order_data = {
        "user_id": 1,
        "price": 100.0,
        "ticket_type": "duo"
    }
    order_response = client.post("/order/", json=order_data)
    assert order_response.status_code in [200, 201], f"Erreur: {order_response.json()}"

    order_id = order_response.json().get("order_id")
    assert order_id, "order_id est absent de la réponse"

    # Étape 2 : Créer un ticket lié à cette commande
    ticket_data = {
        "order_id": order_id,
        "is_single": False,
        "is_duo": True,
        "number_of_places": 2
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code in [200, 201], f"Erreur: {response.json()}"
    assert "application/json" in response.headers["content-type"]
    assert response.json().get("is_duo") is True