from datetime import datetime
from app.core.schemas.base import BaseModel

class ActivityCreateDTO(BaseModel):
    user_id: int
    activity_date: datetime
    actions: int