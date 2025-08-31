from typing import Optional

from app.core.schemas.base import BaseModel
from app.core.enums import UserRole

class UserCreateDTO(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: Optional[str] = None
    language: str
    role: UserRole
    
class UserUpdateDTO(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language: str | None = None
    is_alive: bool | None = None
    banned: bool | None = None
    
class UserReadDTO(UserCreateDTO):
    id: int
    is_alive: bool
    banned: bool