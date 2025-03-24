from pydantic import BaseModel
from datetime import datetime as datetime


# Schéma pour créer ou mettre à jour une commande
class OrderCreate(BaseModel):
    user_id: int
    ticket_id: int
    date_order: datetime
    prix: float

# Schéma pour les réponses (incluant l'ID)
class OrderResponse(OrderCreate):
    order_id: int

    class Config:
        from_attributes = True