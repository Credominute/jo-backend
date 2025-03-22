from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    ticket_id = Column(Integer, ForeignKey("ticket.ticket_id"))
    date_order = Column(DateTime, default=datetime.now)
    price = Column(Float)  # Ajout de la colonne prix, en fonction du billet commandé
    user = relationship ("User")
    ticket = relationship ("Ticket")