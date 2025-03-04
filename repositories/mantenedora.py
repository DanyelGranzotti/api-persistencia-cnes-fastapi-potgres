from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.mantenedora import Mantenedora
from typing import List

class MantenedoraRepository(BaseRepository[Mantenedora]):
    def __init__(self, session):
        super().__init__(session, Mantenedora)

    async def create(self, data: dict) -> Mantenedora:
        try:
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            await self.session.rollback()
            if 'mantenedoras_cnpj_mantenedora_key' in str(e):
                raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
            raise HTTPException(status_code=400, detail="Erro ao criar mantenedora")

    async def get_all(self) -> list[Mantenedora]:
        query = select(self.model).options(selectinload(self.model.estabelecimentos))
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, id: int) -> Mantenedora:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, id: int, data: dict) -> Mantenedora:
        try:
            query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except IntegrityError as e:
            await self.session.rollback()
            if 'mantenedoras_cnpj_mantenedora_key' in str(e):
                raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
            raise HTTPException(status_code=400, detail="Erro ao atualizar mantenedora")
    
    async def delete(self, id: int):
        query = self.model.__table__.delete().where(self.model.id == id)
        await self.session.execute(query)
        await self.session.flush()

    async def get_by_filters(self, filters: dict) -> List[Mantenedora]:
        query = select(Mantenedora)
        for key, value in filters.items():
            query = query.where(getattr(Mantenedora, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(Mantenedora)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_paginated(self, limit: int, offset: int) -> List[Mantenedora]:
        query = select(Mantenedora).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()