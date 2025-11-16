from pydantic import BaseModel,EmailStr
from datetime import date
from typing import Optional

from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[date] = None
    
    model_config = {"from_attributes": True}
    
class PostResponse(PostBase):
    created_at: Optional[date] = None
    id: int
    owner_id: int
    owner: 'UserResponse'
    
    model_config = {"from_attributes": True}

class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int  # 1 for upvote, 0 for removing vote

class VoteResponse(BaseModel):
    post_id: int
    user_id: int