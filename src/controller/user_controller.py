from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.model.user import User
from src.schema.login_schema import UserLogin
from src.schema.user_schema import UserCreate
from src.config.hash import pwd_context
from src.service.auth_service import get_user_by_mail, get_user_by_nom
from src.service.token_service import create_token

USER_NOT_FOUND_MSG = "User not found"
# vérification de l'existence d'un utilisateur par son mail
def verify_user(mail: str, db: Session):
    db_user = db.query(User).filter(User.mail == mail).first()
    if db_user:
        return {"exists": True}
    return {"exists": False}

# création d'un utilisateur
def create_user(user: UserCreate,db: Session):
    # Vérifier si le nom existe déjà (logique lors de la création)
    db_user = get_user_by_nom(db=db,
                              nom=user.nom)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà utilisé."
        )
    # Hash du mot de passe
    mdp_hache = pwd_context.hash(user.mot_de_passe)
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        mail=user.mail,
        telephone=user.telephone,
        mot_de_passe=mdp_hache
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# modèle de login standard par mail et mot_de_passe
def login_user(user: UserLogin, db: Session):
    db_user = get_user_by_mail(db=db, mail=user.mail)  # Utiliser mail au lieu de nom
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adresse mail non existante."  # Message adapté
        )
    # Vérification du mot de passe
    if pwd_context.verify(user.mot_de_passe, db_user.mot_de_passe):
        return create_token(data={"sub": user.mail})  # Utiliser mail pour le token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect."
        )

# lecture d'un utilisateur par son id
def read_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND_MSG)
    return user

# lecture de tous les utilisateurs
def read_user(db:Session):
    return db.query(User).all() # Select all from the user table

# supprimer un utilisateur selon son id
def delete_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND_MSG)
    db.delete(user)
    db.commit()
    return user

# mise à jour d'un utilisateur selon son id
def update_user_by_id(user_id: int, updated_user: UserCreate, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND_MSG)
    for key, value in updated_user.model_dump().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user