from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel

from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.database import Base

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: type[T]
    
    @classmethod
    async def add_one(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        
        session.add(new_instance)
        try:
            await session.flush()
            # await session.refresh()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
    
    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        values_list = [instance.model_dump(exclude_unset=True) for instance in instances]
        new_instances = [cls.model(**values_dict) for values_dict in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances
    
    @classmethod
    async def delete_by_id(cls, session: AsyncSession, data_id: int):
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    
    @classmethod
    async def delete_many(cls, session: AsyncSession, filters: Optional[BaseModel] = None):
        if filters:
            filters_dict = filters.model_dump(exclude_unset=True)
            stmt = (
                delete(cls.model)
                .filter_by(**filters_dict)
            )
        else:
            stmt = (
                delete(cls.model)
            )
        try:
            await session.execute(stmt)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        filters_dict = filters.model_dump(exclude_unset=True)
        stmt = (
            select(cls.model)
            .filter_by(**filters_dict)
        )
        
        try:
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e
        
    @classmethod 
    async def find_by_id(cls, session: AsyncSession, data_id: int):
        try:
            result = await session.get(cls.model, data_id)
            return result
        except SQLAlchemyError as e:
            raise e
    
    @classmethod
    async def find_all(cls, session: AsyncSession, filters: Optional[BaseModel] = None):
        if filters:
            filters_dict = filters.model_dump(exclude_unset=True)
        else:
            filters_dict = {}
            
        stmt = (
            select(cls.model)
            .filter_by(**filters_dict)
        )
        
        try:
            result = await session.execute(stmt)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            raise e
    
    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        try:
            # stmt = (
            #     update(cls.model)
            #     .where(cls.model.id == data_id)
            #     # .filter_by(id=data_id)
            #     .values(**values_dict)
            # )
            record = await session.get(cls.model, data_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    
    @classmethod
    async def update_many(cls, session: AsyncSession, filter_criteria: BaseModel, values: BaseModel):
        filters_dict = filter_criteria.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        try:
            stmt = (
                update(cls.model)
                .filter_by(**filters_dict)
                .values(**values_dict)
            )
            records = await session.execute(stmt)
            return records.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise e