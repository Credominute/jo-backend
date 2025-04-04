from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.order import Order
from src.model.ticket import Ticket
from src.schema.order_schema import OrderCreate

# création d'une commande
def create_order_with_ticket(order: OrderCreate, db: Session):
    db_order = Order(
        user_id=order.user_id,
        price=order.price,
        ticket_type=order.ticket_type
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Créer les billets associés à la commande
    ticket_count = 1  # Par défaut pour un ticket simple
    number_of_places = 1  # Nombre de places par billet par défaut

    # Modifier en fonction du type de billet
    if order.ticket_type == "duo":
        ticket_count = 2  # 2 billets pour un duo
        number_of_places = 2  # Chaque billet a 2 places
    elif order.ticket_type == "famille":
        ticket_count = 4  # 4 billets pour une commande familiale
        number_of_places = 4  # Chaque billet a 4 places
    elif order.ticket_type != "simple":
        raise HTTPException(status_code=400, detail="Invalid ticket type")

    tickets = []
    # Créer les billets avec le nombre approprié de places
    for _ in range(ticket_count):
        db_ticket = Ticket(
            order_id=db_order.order_id,
            is_single=order.ticket_type == "simple",
            is_duo=order.ticket_type == "duo",
            is_familial=order.ticket_type == "famille",
            number_of_places=number_of_places  # Utilisation de number_of_places spécifique à chaque billet
        )
        db.add(db_ticket)
        tickets.append(db_ticket)

    db.commit()

    # Retourner la commande et les tickets
    return db_order, tickets

# lecture d'une commande par son id
def read_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404,
                            detail="order not found")
    return order