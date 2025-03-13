from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controller.user_controller import read_user, read_user_by_id, delete_user_by_id, create_user, update_user_by_id
from src.schema.user_schema import UserCreate, UserResponse


class UserApi:

    def __init__(self):
        self.router = APIRouter()
        self.add_routes()

    def add_routes(self):

        @self.router.post("/", response_model=UserResponse)
        def create_user_endpoint(user:UserCreate, db: Session = Depends(get_db)):
            return create_user(user,db)

        @self.router.get("/", response_model=List[UserResponse])
        def read_user_endpoint(db: Session = Depends(get_db)):
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