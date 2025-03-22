from sqlalchemy import Column, Integer, Boolean
from src.config.database import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    is_single = Column(Boolean, default=False) # usage de booléens ici, plus simple qu'une énumération
    is_duo = Column(Boolean, default=False)
    is_familial = Column(Boolean, default=False)
