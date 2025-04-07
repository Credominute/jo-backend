from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model.order import Order
from src.schema.order_schema import OrderWithTicketsResponse
from src.model.ticket import Ticket
from src.schema.order_schema import OrderCreate
from src.schema.ticket_schema import TicketResponse


# création d'une commande
def create_order_with_ticket(order_data: OrderCreate, db: Session) -> OrderWithTicketsResponse:

    # 1. Créer la commande
    order_model = Order(
        user_id=order_data.user_id,
        price=order_data.price,
        ticket_type=order_data.ticket_type
    )
    db.add(order_model)
    db.commit()
    db.refresh(order_model)

    # 2. Créer des tickets associés
    tickets = []
    if order_model.ticket_type == "SIMPLE":
        ticket = Ticket(order_id=order_model.order_id, is_single=True, number_of_places=1)
        tickets.append(ticket)
    elif order_model.ticket_type == "DUO":
        # Créer deux billets pour un ticket de type "DUO"
        ticket1 = Ticket(order_id=order_model.order_id, is_duo=True, number_of_places=1)
        ticket2 = Ticket(order_id=order_model.order_id, is_duo=True, number_of_places=1)
        tickets.extend([ticket1, ticket2])
    elif order_model.ticket_type == "FAMILIAL":
        ticket = Ticket(order_id=order_model.order_id, is_familial=True, number_of_places=4)
        tickets.append(ticket)
    else:
        raise ValueError("Type de ticket invalide")

    # Ajouter les tickets à la base de données
    for ticket in tickets:
        db.add(ticket)
    db.commit()

    # Rafraîchir les tickets pour récupérer les IDs
    for ticket in tickets:
        db.refresh(ticket)

    # Créer les réponses pour chaque ticket
    ticket_responses = []
    for ticket in tickets:
        ticket_responses.append(TicketResponse(
            ticket_id=ticket.ticket_id,
            order_id=ticket.order_id,
            is_single=ticket.is_single,
            is_duo=ticket.is_duo,
            is_familial=ticket.is_familial,
            number_of_places=ticket.number_of_places
        ))

    # Retourner la commande avec les tickets
    return OrderWithTicketsResponse(
        order_id=order_model.order_id,
        user_id=order_model.user_id,
        price=order_model.price,
        ticket_type=order_data.ticket_type,
        tickets=ticket_responses
    )

# lecture d'une commande par son id
def read_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="order not found")
    return order


