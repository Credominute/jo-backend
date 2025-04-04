from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from src.config.database import Base

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), unique =True)
    date_order = Column(DateTime, default=datetime.now)
    price = Column(Float)  # Le prix total pour la commande
    ticket_type = Column(String(10), nullable=False) # le type "single", "duo" ou "familial"

    user = relationship ("User", back_populates="orders")
    tickets = relationship ("Ticket", back_populates="order", cascade="all, delete-orphan")