from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.controller.ticket_controller import read_ticket, read_ticket_by_id, delete_ticket_by_id, create_ticket, update_ticket_by_id
from src.schema.ticket_schema import TicketCreate, TicketResponse
from src.service.token_service import verify_token

class TicketApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=TicketResponse)
        def create_ticket_endpoint(ticket: TicketCreate, request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return create_ticket(ticket, db)

        @self.router.get("/", response_model=List[TicketResponse])
        def read_tickets_endpoint(db: Session = Depends(get_db)):
            return read_ticket(db)

        @self.router.get("/{ticket_id}", response_model=TicketResponse)
        def read_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
            return read_ticket_by_id(ticket_id, db)

        @self.router.delete("/{ticket_id}", response_model=TicketResponse)
        def delete_ticket_endpoint_by_id(ticket_id: int, request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return delete_ticket_by_id(ticket_id, db)

        @self.router.put("/{ticket_id}", response_model=TicketResponse)
        def update_ticket_endpoint_by_id(ticket_id: int,
                                         update_ticket: TicketCreate,
                                         request: Request,
                                         db: Session = Depends(get_db)):
            verify_token(request)
            return update_ticket_by_id(ticket_id, update_ticket, db)