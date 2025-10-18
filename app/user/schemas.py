from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True
        

    
