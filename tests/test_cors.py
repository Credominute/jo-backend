import pytest
from fastapi.testclient import TestClient
from main import app  # Votre fichier main.py où l'application est définie

client = TestClient(app)

def test_cors_enabled():
    # Simulation d'une requête avec une origine différente
    response = client.get("/ping", headers={"Origin": "http://example.com"})
    headers = response.headers

    # Vérification que l'en-tête CORS est bien présent
    assert "access-control-allow-origin" in headers, f"Headers: {headers}"