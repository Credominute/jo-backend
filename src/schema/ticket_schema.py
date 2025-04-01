from pydantic import BaseModel


# Schema pour créer ou mettre à jour un billet
class TicketResponse(BaseModel):
    ticket_id: int
    order_id: int
    is_single: bool
    is_duo: bool
    is_familial: bool
    number_of_places: int

    class Config:
        from_attributes = True

# Schema pour créer ou mettre à jour un billet
class TicketCreate(BaseModel):
    is_single: bool
    is_duo: bool
    is_familial: bool
    number_of_places: int

    class Config:
        from_attributes = True

