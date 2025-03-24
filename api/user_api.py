from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.controller.user_controller import create_user, read_user, read_user_by_id, delete_user_by_id, update_user_by_id
from src.schema.user_schema import UserCreate, UserResponse
from src.service.token_service import verify_token

class UserApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=UserResponse)
        def create_user_endpoint(user: UserCreate, request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return create_user(user, db)

        @self.router.get("/", response_model=List[UserResponse])
        def read_users_endpoint(request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return read_user(db)

        @self.router.get("/{user_id}", response_model=UserResponse)
        def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
            return read_user_by_id(user_id, db)

        @self.router.delete("/{user_id}", response_model=UserResponse)
        def delete_user_endpoint_by_id(user_id: int, request: Request, db: Session = Depends(get_db)):
            verify_token(request)
            return delete_user_by_id(user_id, db)

        @self.router.put("/{ticket_id}", response_model=UserResponse)
        def update_user_endpoint_by_id(user_id: int,
                                       update_user: UserCreate,
                                       request: Request,
                                       db: Session = Depends(get_db)):
            verify_token(request)
            return update_user_by_id(user_id, update_user, db)