from pydantic import BaseModel

# Schema pour créer ou mettre à jour un utilisateur
class UserCreate(BaseModel):
    nom: str
    prenom: str
    mail: str
    telephone: int
    mot_de_passe: str

# Schema pour les réponses (incluant l'ID)
class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True
