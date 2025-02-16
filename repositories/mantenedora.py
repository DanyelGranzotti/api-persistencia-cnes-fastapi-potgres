from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.mantenedora import Mantenedora

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
