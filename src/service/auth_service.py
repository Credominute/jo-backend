from typing import Optional

from sqlalchemy.orm import Session

from src.model.viewer import Viewer


def get_viewer_by_username(username: str, db:Session) -> Optional[Viewer]:
    return db.query(Viewer).filter(Viewer.username == username).first()
