from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db

from src.controller.user_controller import read_user, read_user_by_id, delete_user_by_id, create_user, update_user_by_id
from src.controller.ticket_controller import read_ticket, read_ticket_by_id, delete_ticket_by_id, create_ticket, update_ticket_by_id
from src.controller.order_controller import read_order, read_order_by_id, delete_order_by_id, create_order, update_order_by_id

from src.schema.user_schema import UserCreate, UserResponse
from src.schema.ticket_schema import TicketCreate, TicketResponse
from src.schema.order_schema import OrderCreate, OrderResponse

# pour les utilisateurs
class UserApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=UserResponse)
        def create_user_endpoint(user:UserCreate, db: Session = Depends(get_db)):
            return create_user(user,db)

        @self.router.get("/", response_model=List[UserResponse])
        def read_users_endpoint(db: Session = Depends(get_db)):
            return read_user(db)

        @self.router.get("/{user_id}", response_model=UserResponse)
        def read_user_endpoint(user_id: int,db: Session = Depends(get_db)):
            return read_user_by_id(user_id,db)

        @self.router.delete("/{user_id}", response_model=UserResponse)
        def delete_user_endpoint_by_id(user_id: int,db: Session = Depends(get_db)):
            return delete_user_by_id(user_id,db)

        @self.router.put("/{user_id}", response_model=UserResponse)
        def update_user_endpoint_by_id(user_id: int,
                                        update_user: UserCreate,
                                        db: Session = Depends(get_db)):
            return update_user_by_id(user_id, update_user, db)

# pour les billets
class TicketApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=TicketResponse)
        def create_ticket_endpoint(ticket: TicketCreate, db: Session = Depends(get_db)):
            return create_ticket(ticket, db)

        @self.router.get("/", response_model=List[TicketResponse])
        def read_tickets_endpoint(db: Session = Depends(get_db)):
            return read_ticket(db)

        @self.router.get("/{ticket_id}", response_model=TicketResponse)
        def read_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
            return read_ticket_by_id(ticket_id, db)

        @self.router.delete("/{ticket_id}", response_model=TicketResponse)
        def delete_ticket_endpoint_by_id(ticket_id: int, db: Session = Depends(get_db)):
            return delete_ticket_by_id(ticket_id, db)

        @self.router.put("/{ticket_id}", response_model=TicketResponse)
        def update_ticket_endpoint_by_id(ticket_id: int,
                                         update_ticket: TicketCreate,
                                         db: Session = Depends(get_db)):
            return update_ticket_by_id(ticket_id, update_ticket, db)

# pour les commandes
class OrderApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=OrderResponse)
        def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
            return create_order(order, db)

        @self.router.get("/", response_model=List[OrderResponse])
        def read_orders_endpoint(db: Session = Depends(get_db)):
            return read_order(db)

        @self.router.get("/{order_id}", response_model=OrderResponse)
        def read_order_endpoint(order_id: int, db: Session = Depends(get_db)):
            return read_order_by_id(order_id, db)

        @self.router.delete("/{order_id}", response_model=OrderResponse)
        def delete_order_endpoint_by_id(order_id: int, db: Session = Depends(get_db)):
            return delete_order_by_id(order_id, db)

        @self.router.put("/{order_id}", response_model=OrderResponse)
        def update_order_endpoint_by_id(order_id: int,
                                        update_order: OrderCreate,
                                        db: Session = Depends(get_db)):
            return update_order_by_id(order_id, update_order, db)