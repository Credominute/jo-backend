from pydantic import BaseModel


# Schéma pour créer ou mettre à jour une commande
class OrderCreate(BaseModel):
    user_id: int
    price: float
    ticket_type: str  # Qui peut être, 'simple', 'duo', 'famille'

    class Config:
        from_attributes = True
