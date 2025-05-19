from pydantic import BaseModel

class UserLogin(BaseModel):
    mail: str
    mot_de_passe: str
