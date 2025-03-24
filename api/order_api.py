from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.controller.order_controller import read_order_by_id, create_order
from src.schema.order_schema import OrderCreate, OrderResponse
from src.service.token_service import verify_token

class OrderApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=OrderResponse)
        def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
            return create_order(order, db)

        @self.router.get("/{order_id}", response_model=OrderResponse)
        def read_order_endpoint(order_id: int, request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return read_order_by_id(order_id, db)
