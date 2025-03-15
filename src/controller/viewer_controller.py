from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from src.config.hash import pwd_context
from src.model import viewer
from src.model.viewer import Viewer
from src.service.auth_service import get_viewer_by_username
from src.schema.viewer_schema import ViewerCreate
from src.service.token_service import create_token


def create_viewer(viewer: ViewerCreate, db: Session):
    db_viewer = get_viewer_by_username(db=db,
                                   username=viewer.username)
    if db_viewer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà utilisé."
        )
    hashed_password = pwd_context.hash(viewer.password)
    new_viewer = Viewer(username=viewer.username,
                        hashed_password=hashed_password)
    db.add(new_viewer)
    db.commit()
    db.refresh(new_viewer)
    return(new_viewer)


def login_viewer(viewer: ViewerCreate, db: Session):

   #1. je récupère mon utilisateur en base
   db_viewer = get_viewer_by_username(db=db,
                                      username=viewer.username)

   #2. je vérifie qu'il n'est pas "None"
   if not db_viewer:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Nom d'utilisateur non existant"
       )

   #3. je compare le password
   if pwd_context.verify(viewer.password, db_viewer.hashed_password):
       return create_token(data={"sub": viewer.username})
   else:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Mot de passe incorrect"
       )