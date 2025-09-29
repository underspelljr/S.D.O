import uuid
from pydantic import BaseModel, ConfigDict

# Base schema with shared attributes
class UserBase(BaseModel):
    name: str

# Schema for creating a user
class UserCreate(UserBase):
    pass

# Schema for reading a user (from API)
class User(UserBase):
    id: int
    uuid: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

class UserSimple(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)