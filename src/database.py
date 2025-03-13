from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://credominute_mercadona:oTvw10jUDkTWqfVP@postgresql-credominute.alwaysdata.net:5432/credominute_jo2024"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine)

Base = declarative_base()