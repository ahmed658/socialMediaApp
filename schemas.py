from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
class PostCreate(PostBase):
    pass

class PostReturn(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
#    class Config:
#        orm_mode = True
       
class CreateUser(BaseModel):
    email: EmailStr
    password: str


    
#class LoginUser(CreateUser):
#    pass

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class VoteCreate(BaseModel):
    post_id: int
    vote_dir: conint(ge= -1, le= 1)
    
class VoteReturn(VoteCreate):
    user_id: int