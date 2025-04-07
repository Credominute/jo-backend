from sqlalchemy import create_engine
import pytest

# Définissons l'URL de ma base de données
DATABASE_URL = "postgresql://credominute_mercadona:oTvw10jUDkTWqfVP@postgresql-credominute.alwaysdata.net:5432/credominute_jo2024"

# Créons "l'engine" pour notre connexion
engine = create_engine(DATABASE_URL)

# Testons la connexion à la base de données
def test_database_connection():
    try:
         with engine.connect() as connection:
            print("✅ Connexion réussie à PostgreSQL sur alwaysdata")
            assert connection is not None  # Teste que la connexion n'est pas vide
    except Exception as e:
         pytest.fail(f"❌ Erreur de connexion : {e}")