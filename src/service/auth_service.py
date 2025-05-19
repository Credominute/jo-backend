from sqlalchemy.orm import Session
from src.model.user import User

# Récupérer l'utilisateur par son nom
def get_user_by_nom(db: Session, nom: str):
    return db.query(User).filter(User.nom == nom).first()

# Récupérer l'utilisateur par son mail
def get_user_by_mail(db: Session, mail: str):
    return db.query(User).filter(User.mail == mail).first()