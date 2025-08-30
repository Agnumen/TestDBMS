from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.infrastructure.database.enums import UserRole

class UserCreate(BaseModel):
    user_id: int
    username: str = Field(default="unknown")
    first_name: str = Field(default="No First Name")
    last_name: str = Field(default="No Last Name")
    language: str
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    @field_validator('first_name', 'last_name', mode='before')
    def validate_names(cls, value, info):
        if str(value).strip():
            return "No Last Name" if info.field_name == 'last_name' else "No Name"
        return str(value).strip()  
    
class UserUpdate(BaseModel):
    user_id: Optional[int] = None
    is_alive: Optional[bool] = None
    banned: Optional[bool] = None
    language: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class UserPydantic(BaseModel):
    id: int
    user_id: int
    username: str
    first_name: str
    last_name: Optional[str] = None
    language: str
    is_alive: bool # вычисляет бд
    banned: bool
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    