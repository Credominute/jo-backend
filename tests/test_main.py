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
from fastapi import HTTPException
from src.config.database import Base, engine, SessionLocal
from src.model.order import Order
from src.model.ticket import Ticket
from src.model.user import User
from src.schema.order_schema import OrderCreate
from src.schema.ticket_schema import TicketCreate
from src.schema.user_schema import UserCreate
from src.schema.login_schema import UserLogin
from src.controller.order_controller import create_order_with_ticket
from src.controller.ticket_controller import create_ticket, read_ticket_by_id
from src.controller.user_controller import (
    verify_user,
    create_user as uc_create_user,
    login_user,
    read_user_by_id,
    delete_user_by_id,
    update_user_by_id,
    USER_NOT_FOUND_MSG,
)
from src.service.qrcode_service import generate_qr_code

import uuid
import base64
from io import BytesIO
import qrcode
import pytest

# Préparation de la base
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

#— Tests existants —#

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_redirect_to_docs():
    response = client.get("/api", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"

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
    r = client.post("/user/", json=user_data)
    assert r.status_code == 200
    d = r.json()
    assert d["nom"] == "Dupont"
    assert d["mail"] == mail

def test_create_and_get_order():
    clear_db()
    mail = f"user_{uuid.uuid4().hex[:8]}@ex.com"
    # Créer l'utilisateur
    u = {
        "nom": "Test",
        "prenom": "User",
        "mail": mail,
        "telephone": "1234567890",
        "mot_de_passe": "testpassword"
    }
    ur = client.post("/user/", json=u)
    assert ur.status_code == 200
    uid = ur.json().get("user_id")
    assert uid
    # Créer la commande DUO
    od = {"user_id": uid, "price": 100.0, "ticket_type": "DUO"}
    cr = client.post("/order/", json=od)
    assert cr.status_code in (200, 201)
    co = cr.json()
    oid = co["order_id"]
    assert oid
    assert co["ticket_type"] == "DUO"
    assert len(co.get("tickets", [])) == 2
    assert all(t["is_duo"] for t in co["tickets"])
    # Récupérer la commande
    gr = client.get(f"/order/{oid}")
    assert gr.status_code == 200
    go = gr.json()
    assert go["ticket_type"] == "DUO"
    assert len(go.get("tickets", [])) == 2

def test_ticket_endpoint():
    r = client.get("/ticket")
    assert r.status_code == 200
    assert "application/json" in r.headers["content-type"]

def test_create_ticket_via_api():
    clear_db()
    mail = f"user_{uuid.uuid4().hex[:8]}@ex.com"
    u = {"nom":"Test","prenom":"User","mail":mail,"telephone":"1234567890","mot_de_passe":"testpassword"}
    ur = client.post("/user/", json=u); uid = ur.json()["user_id"]
    lr = client.post("/auth/login", json={"mail":mail,"mot_de_passe":"testpassword"})
    token = lr.json().get("access_token")
    assert token
    od = {"user_id": uid, "price": 100.0, "ticket_type": "DUO"}
    create_order_resp = client.post("/order/", json=od)
    assert create_order_resp.status_code in (200, 201)
    oid = create_order_resp.json()["order_id"]
    td = {"order_id": oid, "is_single": False, "is_duo": True, "is_familial": False, "number_of_places": 2}
    tr = client.post("/ticket", json=td, headers={"Authorization":f"Bearer {token}"})
    assert tr.status_code in (200,201)
    t = tr.json()
    assert t["order_id"] == oid
    assert t["is_duo"] and not t["is_familial"]
    assert t["number_of_places"] == 2

def test_register_and_login_flow():
    clear_db()
    ud = {
        "nom": "Test",
        "prenom": "Auth",
        "mail": f"auth_{uuid.uuid4().hex[:8]}@ex.com",
        "telephone": "0102030405",
        "mot_de_passe": "SecurePass123!"
    }
    rr = client.post("/auth/register", json=ud)
    assert rr.status_code == 200
    ru = rr.json()
    assert ru["mail"] == ud["mail"] and "user_id" in ru
    lr = client.post("/auth/login", json={"mail":ud["mail"],"mot_de_passe":ud["mot_de_passe"]})
    assert lr.status_code == 200 and lr.json().get("access_token")
    br = client.post("/auth/login", json={"mail":ud["mail"],"mot_de_passe":"bad"})
    assert br.status_code in (400,401)
    nr = client.post("/auth/login", json={"mail":"no@user","mot_de_passe":"any"})
    assert nr.status_code in (400,401)

#— Nouveaux tests de services et contrôleurs —#

def test_generate_qr_code_service():
    data = "hello"
    b64 = generate_qr_code(data)
    raw = base64.b64decode(b64)
    # Vérifier header PNG
    assert raw.startswith(b"\x89PNG\r\n\x1a\n")
    # Générer image de référence
    img = qrcode.make(data)
    buf = BytesIO(); img.save(buf, format="PNG")
    assert raw == buf.getvalue()

def test_create_and_read_ticket_controller(db_session=SessionLocal()):
    # 0) Créer un utilisateur pour avoir un user_id valide
    from src.model.user import User
    from src.config.hash import pwd_context

    raw_pw = "dummy"
    user = User(
        nom="Tmp",
        prenom="User",
        mail="tmp@example.com",
        telephone="0000000000",
        mot_de_passe=pwd_context.hash(raw_pw)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.user_id

    # 1) Créer la commande liée à ce user
    from src.controller.order_controller import create_order_with_ticket
    order_data = OrderCreate(user_id=user_id, price=10.0, ticket_type="SIMPLE")
    order_resp = create_order_with_ticket(order_data, db_session)
    order_id = order_resp.order_id

    # 2) Création du ticket
    tc = TicketCreate(
        order_id=order_id,
        is_single=True, is_duo=False, is_familial=False,
        number_of_places=1
    )
    t = create_ticket(tc, db_session)
    assert t.ticket_id is not None

    # 3) Lecture et QR Code
    rd = read_ticket_by_id(t.ticket_id, db_session)
    assert rd["ticket_id"] == t.ticket_id
    assert "qrcode" in rd
    with pytest.raises(HTTPException):
        read_ticket_by_id(0, db_session)


def test_user_controller_crud(db_session=SessionLocal()):
    # verify_user
    assert verify_user("x@y.com", db_session) == {"exists": False}
    # create_user & read_user_by_id
    uc = UserCreate(nom="N", prenom="P", mail="u@x.com", telephone="0", mot_de_passe="pw")
    user = uc_create_user(uc, db_session)
    fetched = read_user_by_id(user.user_id, db_session)
    assert fetched.mail == "u@x.com"
    # login_user
    tok = login_user(UserLogin(mail="u@x.com", mot_de_passe="pw"), db_session)
    assert hasattr(tok, "access_token")
    with pytest.raises(HTTPException):
        login_user(UserLogin(mail="u@x.com", mot_de_passe="bad"), db_session)
    # update & delete
    uc2 = UserCreate(nom="N", prenom="Q", mail="u@x.com", telephone="1", mot_de_passe="pw")
    upd = update_user_by_id(user.user_id, uc2, db_session)
    assert upd.prenom == "Q"
    deleted = delete_user_by_id(user.user_id, db_session)
    assert deleted.user_id == user.user_id
    with pytest.raises(HTTPException):
        delete_user_by_id(user.user_id, db_session)