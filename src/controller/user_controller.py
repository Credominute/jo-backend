from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.model import user
from src.model.user import User, UserRole
from src.schema.login_schema import UserLogin
from src.schema.user_schema import UserCreate
from src.config.hash import pwd_context
from src.service.auth_service import get_user_by_mail, get_user_by_nom
from src.service.token_service import create_token

ADMIN_EMAIL = "admin@hotmail.com"
USER_NOT_FOUND_MSG = "User not found"

# vérification de l'existence d'un utilisateur par son mail
def verify_user(mail: str, db: Session):
    db_user = db.query(User).filter(User.mail == mail).first()
    return {"exists": db_user is not None}

# création d'un utilisateur
def create_user(user_data: UserCreate, db: Session):
    # Vérifier si le nom existe déjà
    db_user = get_user_by_nom(db=db, nom=user_data.nom)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà utilisé."
        )

    # Déterminer le rôle en fonction de l'email
    role = UserRole.admin if user_data.mail == ADMIN_EMAIL else UserRole.user

    # Hash du mot de passe
    mdp_hache = pwd_context.hash(user_data.mot_de_passe)

    new_user = User(
        nom=user_data.nom,
        prenom=user_data.prenom,
        mail=user_data.mail,
        telephone=user_data.telephone,
        mot_de_passe=mdp_hache,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# modèle de login standard par mail et mot_de_passe
def login_user(login_data: UserLogin, db: Session):
    db_user = get_user_by_mail(db=db, mail=login_data.mail)  # Utiliser mail au lieu de nom
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adresse mail non existante."  # Message adapté
        )
    # Vérification du mot de passe
    if pwd_context.verify(login_data.mot_de_passe, db_user.mot_de_passe):
        return create_token(data={"sub": db_user.mail})  # Utiliser mail pour le token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect."
        )

# lecture d'un utilisateur par son id
def read_user_by_id(user_id: int, db: Session):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND_MSG)
    return db_user

# lecture de tous les utilisateurs
def read_user(db:Session):
    return db.query(User).all() # Select all from the user table

# supprimer un utilisateur selon son id
def delete_user_by_id(user_id: int, db: Session):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND_MSG)
    db.delete(db_user)
    db.commit()
    return db_user


# mise à jour d'un utilisateur selon son id
def update_user_by_id(user_id: int, updated_user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MSG)
    for key, value in updated_user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user