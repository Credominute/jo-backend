from pydantic import BaseModel, ConfigDict
from typing import Optional

# Schema pour créer ou mettre à jour un billet
class TicketResponse(BaseModel):
    ticket_id: int
    order_id: int
    is_single: bool
    is_duo: bool
    is_familial: bool
    number_of_places: int
    qrcode: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Schema pour créer ou mettre à jour un billet
class TicketCreate(BaseModel):
    order_id: int
    is_single: bool
    is_duo: bool
    is_familial: bool
    number_of_places: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)