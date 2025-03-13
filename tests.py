from sqlalchemy import create_engine

DATABASE_URL = "postgresql://credominute_mercadona:oTvw10jUDkTWqfVP@postgresql-credominute.alwaysdata.net:5432/credominute_jo2024"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("✅ Connexion réussie à PostgreSQL sur alwaysdata")
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")