from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controller.user_controller import create_user, login_user
from src.schema.login_schema import UserLogin
from src.schema.token_schema import Token
from src.schema.user_schema import UserResponse, UserCreate

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_viewer(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user,db)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Appel de la fonction login pour obtenir le token
    return login_user(user,db)