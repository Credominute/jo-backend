from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controller.viewer_controller import create_viewer, login_viewer
from src.schema.token_schema import Token
from src.schema.viewer_schema import ViewerResponse, ViewerCreate

router = APIRouter()

@router.post("/register", response_model=ViewerResponse)
def register_viewer(viewer: ViewerCreate, db: Session = Depends(get_db)):
    return create_viewer(viewer,db)

@router.post("/", response_model=Token)
def login(viewer: ViewerCreate, db: Session = Depends(get_db)):
 return login_viewer(viewer,db)
