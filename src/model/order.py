from sqlalchemy import Column, Integer, DateTime, Float
from src.config.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, foreign_key=True)
    id_ticket = Column(Integer, foreign_key=True)
    date_order = Column(DateTime, default=datetime.now)
    prix = Column(Float)  # Ajout de la colonne prix, en fonction du billet commandé