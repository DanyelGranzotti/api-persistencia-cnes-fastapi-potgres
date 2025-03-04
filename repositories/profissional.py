from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.profissional import Profissional
from typing import List

class ProfissionalRepository(BaseRepository[Profissional]):
    def __init__(self, session):
        super().__init__(session, Profissional)

    async def create(self, data: dict) -> Profissional:
        try:
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            await self.session.rollback()
            if 'profissionais_codigo_profissional_sus_key' in str(e):
                raise HTTPException(status_code=400, detail="Código do profissional SUS já cadastrado")
            raise HTTPException(status_code=400, detail="Erro ao criar profissional")

    async def get_all(self) -> list[Profissional]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_id(self, id: int) -> Profissional:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, id: int, data: dict) -> Profissional:
        try:
            query = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except IntegrityError as e:
            await self.session.rollback()
            if 'profissionais_codigo_profissional_sus_key' in str(e):
                raise HTTPException(status_code=400, detail="Código do profissional SUS já cadastrado")
            raise HTTPException(status_code=400, detail="Erro ao atualizar profissional")
    
    async def delete(self, id: int):
        query = self.model.__table__.delete().where(self.model.id == id)
        await self.session.execute(query)
        await self.session.flush()

    async def get_by_filters(self, filters: dict) -> List[Profissional]:
        query = select(Profissional)
        for key, value in filters.items():
            query = query.where(getattr(Profissional, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_total_count(self) -> int:
        query = select(func.count()).select_from(Profissional)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_paginated(self, limit: int, offset: int) -> List[Profissional]:
        query = select(Profissional).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()