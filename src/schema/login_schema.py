from pydantic import BaseModel

class UserLogin(BaseModel):
    nom: str
    mot_de_passe: str
