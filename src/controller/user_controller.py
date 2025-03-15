from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.user import User
from src.schema.user_schema import UserCreate

# création d'un utilisateur
def create_user(user: UserCreate,db: Session):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# lecture d'un utilisateur par son id
def read_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return user

# lecture de tous les utilisateurs
def read_user(db:Session):
    return db.query(User).all() # select * from user

# supprimer un utilisateur selon son id
def delete_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")
    db.delete(user)
    db.commit()
    return user

# mise à jour d'un utilisateur selon son id
def update_user_by_id(user_id: int, updated_user: UserCreate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user