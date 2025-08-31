from typing import List, Any, Optional

from sqlalchemy import select, func, desc
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models import Activity
# from app.core.schemas import ActivityCreateDTO

class ActivityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def add_user_activity(self, user_id: int) -> None:
        stmt = (
            pg_insert(Activity)
            .values(user_id=user_id)
            .on_conflict_do_update(
                # constraint="idx_activity_user_day",
                index_elements=["user_id", "activity_date"],
                set_={'actions': Activity.actions + 1}
            )
        )
        await self._session.execute(stmt)
        
        # today = datetime.today()
        # stmt = (
        #     select(Activity)
        #     .filter(Activity.user_id == user_id, Activity.activity_date == today)
        # )
        # result = await self._session.execute(stmt)
        # respond = result.scalar_one_or_none()
        # if respond is not None:
        #     respond.actions += 1
        # else:
        #     self._session.add(Activity(ActivityCreateDTO(user_id=user_id, activity_date=today, actions=1)))
        # await self._session.flush()
        
    async def get_statistics(self) -> Optional[List[tuple[Any, ...]]]:
        stmt = (
            select(Activity.user_id, func.sum(Activity.actions).label("total"))
            .group_by(Activity.user_id)
            .order_by(desc("total"))
            .limit(5)
        )
        result = await self._session.execute(stmt)
        return result.all()
    
"""
add_user_activity
get_statistics
"""