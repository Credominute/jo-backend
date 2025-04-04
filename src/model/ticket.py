from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))  # Clé étrangère vers la commande
    is_single = Column(Boolean, default=False) # usage de booléens ici, plus simple qu'une énumération
    is_duo = Column(Boolean, default=False)
    is_familial = Column(Boolean, default=False)
    number_of_places= Column(Integer, default=1) # Le nombre de places (1 pour simple, 2 pour duo, 4 pour familial)

    # Relation avec la commande
    order = relationship("Order", back_populates="tickets")