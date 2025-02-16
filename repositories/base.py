from typing import Generic, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.exceptions import DatabaseError, DatabaseValidationError, EstabelecimentoError
from models.base import BaseModel

# T representa qualquer modelo que herda de BaseModel
T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Repositório genérico para operações no banco de dados"""
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self.session.execute(select(self.model).filter_by(id=id))
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> T:
        try:
            instance = self.model(**data)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except IntegrityError as e:
            await self.session.rollback()
            error_code = getattr(e.orig, 'pgcode', None)
            if error_code == DatabaseError.UNIQUE_VIOLATION:
                constraint = getattr(e.orig, 'constraint_name', None)
                error_message = EstabelecimentoError.UNIQUE_VIOLATION_MAPPING.get(
                    constraint, 
                    "Violação de restrição única" 
                )
                raise DatabaseValidationError(error_message)
            raise e

    async def update(self, id: int, data: dict) -> Optional[T]:
        try:
            instance = await self.get_by_id(id)
            if not instance:
                return None
                
            for key, value in data.items():
                setattr(instance, key, value)
                
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except IntegrityError as e:
            await self.session.rollback()
            error_code = getattr(e.orig, 'pgcode', None)
            if error_code == DatabaseError.UNIQUE_VIOLATION:
                constraint = getattr(e.orig, 'constraint_name', None)
                error_message = EstabelecimentoError.UNIQUE_VIOLATION_MAPPING.get(
                    constraint, 
                    "Violação de restrição única"
                )
                raise DatabaseValidationError(error_message)
            raise e

    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False
            
        await self.session.delete(instance)
        await self.session.commit()
        return True
