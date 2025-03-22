from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.model.user import User
from src.schema.user_schema import UserCreate

from src.config.hash import pwd_context
from src.service.auth_service import get_user_by_nom
from src.service.token_service import create_token

# création d'un utilisateur
def create_user(user: UserCreate,db: Session):
    db_user = get_user_by_nom(db=db,
                              nom=user.nom)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà utilisé."
        )
    mdp_hache = pwd_context.hash(user.mot_de_passe)
    new_user = User(nom=user.nom,
                    mdp_hache=mdp_hache)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return(new_user)

def login_user(user: UserCreate, db: Session):
   db_user = get_user_by_nom(db=db,
                             nom=user.nom)
   if not db_user:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Nom d'utilisateur non existant."
       )
   if pwd_context.verify(user.mot_de_passe, db_user.mdp_hache):
       return create_token(data={"sub": user.nom})
   else:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Mot de passe incorrect."
       )

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
    for key, value in updated_user.model_dump().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
