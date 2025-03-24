from sqlalchemy import Column, Integer, String
from src.config.database import Base

class User(Base):
    __tablename__ = 'user' # client en français
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), unique=True, index=True, nullable=False)
    prenom = Column(String(50), index=True)
    mail = Column(String(50), unique = True)
    telephone = Column(String(10))
    mot_de_passe = Column(String(255), nullable=False)