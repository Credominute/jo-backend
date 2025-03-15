from pydantic import BaseModel
from datetime import datetime


# Schéma pour créer ou mettre à jour une commande
class OrderCreate(BaseModel):
    date_order: datetime
    prix: float

# Schéma pour les réponses (incluant l'ID)
class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes = True