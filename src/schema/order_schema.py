from enum import Enum
from pydantic import BaseModel, ConfigDict
from src.schema.ticket_schema import TicketResponse
from typing import List

class TicketTypeEnum(str, Enum):
    SINGLE = "SIMPLE"
    DUO = "DUO"
    FAMILIAL = "FAMILIAL"

# Schéma pour créer ou mettre à jour une commande
class OrderCreate(BaseModel):
    user_id: int
    price: float
    ticket_type: TicketTypeEnum  # 'single', 'duo', 'familial'

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    price: float
    ticket_type: TicketTypeEnum
    tickets: List[TicketResponse]  # Liste de tickets associés à la commande

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

class OrderWithTicketsResponse(OrderCreate):
    order_id: int
    tickets: List[TicketResponse]

    model_config = ConfigDict(from_attributes=True)