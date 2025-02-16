from typing import TypeVar, Generic, Type, Union
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_all(self) -> list[ModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> ModelType:
        try:
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            await self.session.commit()
            return entity
        except Exception:
            await self.session.rollback()
            raise

    async def update(self, entity: Union[ModelType, int], data: dict) -> ModelType | None:
        try:
            entity_id = entity if isinstance(entity, int) else entity.id
            query = update(self.model).where(
                self.model.id == entity_id
            ).values(**data).returning(self.model)
            result = await self.session.execute(query)
            updated = result.scalar_one_or_none()
            if updated:
                await self.session.commit()
            return updated
        except Exception:
            await self.session.rollback()
            raise

    async def delete(self, entity: Union[ModelType, int]) -> bool:
        try:
            entity_id = entity if isinstance(entity, int) else entity.id
            query = delete(self.model).where(self.model.id == entity_id)
            result = await self.session.execute(query)
            if result.rowcount > 0:
                await self.session.commit()
                return True
            return False
        except Exception:
            await self.session.rollback()
            raise
