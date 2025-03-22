from sqlalchemy import Column, Integer, String
from src.config.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True, nullable=False)
    prenom = Column(String, index=True)
    mail = Column(String, unique = True)
    telephone = Column(String(15))
    mot_de_passe = Column(String, nullable=False)