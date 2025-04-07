from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controller.order_controller import read_order_by_id, create_order_with_ticket
from src.schema.order_schema import OrderCreate, OrderResponse
from src.schema.ticket_schema import TicketResponse

class OrderApi:
    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=OrderResponse)
        def create_order_endpoint(order_data: OrderCreate, db: Session = Depends(get_db)):
            return create_order_with_ticket(order_data, db)

        @self.router.get("/{order_id}", response_model=OrderResponse)
        def read_order_endpoint(order_id: int, request: Request, db: Session = Depends(get_db)):
            return read_order_by_id(order_id, db)

""" Ancien code : @self.router.post("/", response_model=TicketResponse)
                  def create_order_endpoint(order_data: dict, db: Session = Depends(get_db)):
                      order = OrderCreate(**order_data)
                      return create_order_with_ticket(order, db) """
