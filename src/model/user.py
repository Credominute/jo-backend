from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from src.config.database import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = 'user' # client en français

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), unique=True, index=True, nullable=False)
    prenom = Column(String(50), index=True)
    mail = Column(String(50), unique = True)
    telephone = Column(String(30))
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    # Relation 1:0 avec la commande
    orders = relationship("Order", back_populates="user",
                          uselist=False)  # Un utilisateur peut avoir zéro ou une commande