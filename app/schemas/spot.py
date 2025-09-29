from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.user import UserSimple

# Base schema
class SpotBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None

# Schema for creation
class SpotCreate(SpotBase):
    user_id: int

# Schema for reading (will be returned by the API)
class Spot(SpotBase):
    id: int
    created_by: UserSimple
    
    model_config = ConfigDict(from_attributes=True)