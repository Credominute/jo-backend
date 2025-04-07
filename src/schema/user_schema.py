from pydantic import BaseModel, ConfigDict


# Schema pour créer ou mettre à jour un utilisateur
class UserCreate(BaseModel):
    nom: str
    prenom: str
    mail: str
    telephone: str
    mot_de_passe: str

# Schema pour les réponses (incluant l'ID)
class UserResponse(UserCreate):
    user_id: int

    model_config = ConfigDict(from_attributes=True)