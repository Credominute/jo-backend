from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controller.user_controller import (verify_user, create_user, login_user)
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

@router.get("/verify")
def check_user_existence(mail: str, db: Session = Depends(get_db)):
    result = verify_user(mail, db)
    # On retourne toujours un 200 avec un booléen explicite
    return {"exists": result["exists"]}