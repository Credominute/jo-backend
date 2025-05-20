from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.service.qrcode_service import generate_qr_code
from src.model.ticket import Ticket
from src.schema.ticket_schema import TicketCreate

# création d'un billet
def create_ticket(ticket: TicketCreate,db: Session):
    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# lecture d'un billet par son id
def read_ticket_by_id(ticket_id: int, db: Session):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404,
                            detail=f"ticket with id {ticket_id} not found")
    ticket_data = ticket.to_dict()
    # Générer le QR code et l'ajouter aux données du ticket
    ticket_data['qrcode'] = generate_qr_code(str(ticket.ticket_id))
    return ticket_data

# lecture de tous les billets
def read_ticket(db:Session):
    return db.query(Ticket).all() # select * from ticket

# supprimer un billet selon son id
def delete_ticket_by_id(ticket_id: int, db: Session):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404,
                            detail="ticket not found")
    db.delete(ticket)
    db.commit()
    return ticket

# mise à jour d'un billet selon son id
def update_ticket_by_id(ticket_id: int, updated_ticket: TicketCreate, db: Session):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404,
                            detail="ticket not found")
    for key, value in updated_ticket.model_dump().items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket