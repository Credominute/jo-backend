from pydantic import BaseModel, ConfigDict
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

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
    nom: str
    prenom: str
    mail: str
    telephone: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)