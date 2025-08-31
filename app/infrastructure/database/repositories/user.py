from typing import Optional
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models import User
from app.core.schemas import UserCreateDTO, UserUpdateDTO
from app.core.enums import UserRole

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user_data: UserCreateDTO) -> User:
        user = User(**user_data.model_dump())
        self._session.add(user)
        await self._session.flush()
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_language(self, user_id: int) -> Optional[str]:
        stmt = (
            select(User.language)
            .where(User.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_role(self, user_id: int) -> Optional[UserRole]:
        stmt = (
            select(User.role)
            .filter(User.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_banned_status_by_id(self, user_id: int) -> Optional[bool]:
        stmt = (
            select(User.banned)
            .filter(User.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_banned_status_by_username(self, username: str) -> Optional[bool]:
        stmt = (
            select(User.banned)
            .filter(User.username == username)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_alive_status(self, user_id: int) -> Optional[bool]:
        stmt = (
            select(User.is_alive)
            .filter(User.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
        
    async def change_alive_status(self, user_id: int, is_alive: bool) -> None:
        stmt = (
            update(User)
            .filter(User.user_id == user_id)
            .values(is_alive=is_alive)
        )
        await self._session.execute(stmt)
        # user = await self.get_by_id(user_id)
        # if user:
        #     user.is_alive = is_alive
        #     await self._session.flush()

    async def change_user_banned_status_by_id(self, banned: bool, user_id: int) -> None:
        stmt = (
            update(User)
            .filter(User.user_id == user_id)
            .values(banned=banned)
        )
        await self._session.execute(stmt)

    async def change_user_banned_status_by_username(self, banned: bool, username: str) -> None:
        stmt = (
            update(User)
            .filter(User.username == username)
            .values(banned=banned)
        )
        await self._session.execute(stmt)
            
    async def update_user_lang(self, language: str, user_id: int) -> None:
        stmt = (
            update(User)
            .filter(User.user_id == user_id)
            .values(language=language)
        )
        await self._session.execute(stmt)
    
    
    
            
    async def update_user(self, user: User, update_data: UserUpdateDTO) -> None:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self._session.flush()
            
            
    async def delete_user(self, user_id: int):
        user = await self.get_by_id(user_id=user_id)
        if user:
            await self._session.delete(user)
        
    

"""
add_user DONE
get_user DONE
change_user_alive_status DONE
change_user_banned_status_by_id DONE
change_user_banned_status_by_username DONE
update_user_lang DONE
get_user_lang DONE
get_user_alive_status DONE
get_user_banned_status_by_id DONE
get_user_banned_status_by_username DONE
get_user_role DONE
"""