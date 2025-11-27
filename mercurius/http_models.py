# HTTP Request/Response Schemas
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import datetime as dt
from artisan.artisan import Artisan

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    platform: str = F"{Artisan.get_platform()}"

class TokenRefreshIn(BaseModel):
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: dt.datetime

class ArtifactCreate(BaseModel):
    title: str
    type: str
    content: str

class ArtifactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    type: str
    created_at: dt.datetime
    owner_id: int
    owner: UserOut
    content: Optional[str]
