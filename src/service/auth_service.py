from typing import Optional
from sqlalchemy.orm import Session
from src.model.user import User

def get_user_by_nom(nom: str, db:Session) -> Optional[User]:
    return db.query(User).filter(User.nom == nom).first()
