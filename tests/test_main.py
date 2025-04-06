"""
Tests principaux pour l'application FastAPI.

- `test_ping()`: Vérifie que l'API répond correctement sur `/ping`.
- `test_cors_headers()`: Vérifie que les en-têtes CORS sont bien présents.
- `test_redirect_to_docs()`: Vérifie que `/api` redirige bien vers la documentation.
- `test_user_endpoint()`: Vérifie que l'endpoint `/user` est accessible et renvoie du JSON.
- `test_order_endpoint()`: Vérifie que l'endpoint `/order` est accessible et renvoie du JSON.
- `test_ticket_endpoint()`: Vérifie que l'endpoint `/ticket` est accessible et renvoie du JSON.

Pour les tests en environnement de test, la base de données peut être réinitialisée via :

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
from src.config.database import Base, engine, SessionLocal
from src.model.order import Order
from src.model.ticket import Ticket
from src.model.user import User
import uuid


Base.metadata.create_all(bind=engine)

client = TestClient(app)

def clear_db():
    db = SessionLocal()
    try:
        db.query(Ticket).delete()
        db.query(Order).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

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
    clear_db()
    mail = f"user_{uuid.uuid4().hex[:8]}@ex.com"
    user_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "mail": mail,
        "telephone": "0123456789",
        "mot_de_passe": "testpassword"
    }

    response = client.post("/user/", json=user_data)
    assert response.status_code == 200, f"Erreur: {response.json()}"
    data = response.json()
    assert data["nom"] == "Dupont"
    assert data["mail"] == mail

# Test de création + récupération d'une commande
def test_create_and_get_order():
    clear_db()
    mail = f"user_{uuid.uuid4().hex[:8]}@ex.com"

    # Créer un utilisateur
    user_data = {
        "nom": "Test",
        "prenom": "User",
        "mail": mail,
        "telephone": "1234567890",
        "mot_de_passe": "testpassword"
    }
    user_response = client.post("/user/", json=user_data)
    assert user_response.status_code == 200, f"Erreur création utilisateur: {user_response.json()}"
    user_id = user_response.json().get("user_id")
    assert user_id, "L'ID de l'utilisateur est manquant"

    # Création d'une commande
    order_data = {
        "user_id": user_id,
        "price": 100.0,
        "ticket_type": "DUO"  # "DUO" est en majuscules selon l'énumération
    }
    create_response = client.post("/order/", json=order_data)

    # Vérification de la réponse de création
    assert create_response.status_code in [200, 201], f"Erreur: {create_response.json()}"
    created_order = create_response.json()
    order_id = created_order.get("order_id")
    assert order_id, "order_id est absent de la réponse"

    # Vérifier que le ticket_type est bien retourné en majuscules
    assert created_order.get("ticket_type") == "DUO", f"ticket_type absent ou incorrect: {created_order}"

    # Vérification des billets associés à la commande (on s'attend à 2 billets pour un type DUO)
    assert len(created_order.get("tickets", [])) == 2, f"Nombre de billets incorrect: {created_order.get('tickets')}"

    # Récupération de la commande
    get_response = client.get(f"/order/{order_id}")
    assert get_response.status_code == 200, f"Erreur récupération: {get_response.json()}"
    retrieved_order = get_response.json()

    # Vérification du type de billet dans la commande récupérée
    assert retrieved_order.get("ticket_type") == "DUO", f"ticket_type incorrect: {retrieved_order}"

    # Vérification que les billets sont bien retournés dans la commande récupérée
    assert len(retrieved_order.get("tickets", [])) == 2, f"Nombre de billets incorrect dans la récupération: {retrieved_order.get('tickets')}"
    assert all(ticket['is_duo'] is True for ticket in retrieved_order['tickets']), "Certains billets ne sont pas de type DUO"

# Test de récupération des tickets
def test_ticket_endpoint():
    response = client.get("/ticket")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]

# Test de création d'un ticket lié à une commande

def test_create_ticket():
    clear_db()
    mail = f"user_{uuid.uuid4().hex[:8]}@ex.com"
    # Créer un utilisateur
    user_data = {
        "nom": "Test",
        "prenom": "User",
        "mail": mail,
        "telephone": "1234567890",
        "mot_de_passe": "testpassword"
    }
    user_response = client.post("/user/", json=user_data)
    assert user_response.status_code == 200, f"Erreur création utilisateur: {user_response.json()}"
    user_id = user_response.json().get("user_id")
    assert user_id, "L'ID de l'utilisateur est manquant"

    # Se connecter pour récupérer le token
    login_data = {
        "nom": "Test",
        "mot_de_passe": "testpassword"
    }
    login_response = client.post("/auth/", json=login_data)
    assert login_response.status_code == 200, f"Erreur login: {login_response.json()}"
    token = login_response.json().get("access_token")
    assert token, "Le token d'accès est manquant"

    # Créer une commande en utilisant l'ID de l'utilisateur
    order_data = {
        "user_id": user_id,
        "price": 100.0,
        "ticket_type": "DUO"
    }
    order_response = client.post("/order/", json=order_data)
    assert order_response.status_code in [200, 201], f"Erreur création de la commande: {order_response.json()}"
    order_id = order_response.json().get("order_id")
    assert order_id, "order_id est absent de la réponse"

    # Créer un ticket lié à la commande
    ticket_data = {
        "order_id": order_id,
        "is_single": False,
        "is_duo": True,
        "is_familial": False,
        "number_of_places": 2
    }
    headers = {"Authorization": f"Bearer {token}"}
    ticket_response = client.post("/ticket", json=ticket_data, headers=headers)
    assert ticket_response.status_code in [200, 201], f"Erreur: {ticket_response.text}"
    ticket = ticket_response.json()
    assert ticket["order_id"] == order_id
    assert ticket["is_duo"] is True
    assert ticket["is_familial"] is False
    assert ticket["number_of_places"] == 2