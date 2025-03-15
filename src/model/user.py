from sqlalchemy import Column, Integer, String
from src.config.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), index=True)
    prenom = Column(String(50), index=True)
    mail = Column(String(255), unique = True, index=True)
    telephone = Column(String(15))
    mot_de_passe = Column(String(255))