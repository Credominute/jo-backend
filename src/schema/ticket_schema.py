from pydantic import BaseModel


# Schema pour créer ou mettre à jour un billet
class TicketCreate(BaseModel):
    is_single: bool
    is_duo: bool
    is_familial: bool

# Schéma pour les réponses (incluant l'ID)
class TicketResponse(TicketCreate):
    id: int

    class Config:
        from_attributes = True