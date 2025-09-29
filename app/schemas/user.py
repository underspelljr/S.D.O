import uuid
from pydantic import BaseModel, ConfigDict

# Base schema with shared attributes
class UserBase(BaseModel):
    name: str

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for reading a user (from API)
class User(UserBase):
    id: int
    uuid: uuid.UUID
    is_active: bool
    permission_level: int
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    is_active: bool | None = None
    permission_level: int | None = None

class UserSimple(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)