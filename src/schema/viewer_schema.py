from pydantic import BaseModel

class ViewerBase(BaseModel):
    username: str

class ViewerCreate(ViewerBase):
    password: str

class ViewerResponse(ViewerBase):
    id: int

    class Config:
        from_attributes = True