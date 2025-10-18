from pydantic import BaseModel, Field

class registerUser(BaseModel):
    username: str
    full_name: str
    password: str = Field(..., max_length=72)
    
    
class loginUser(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str