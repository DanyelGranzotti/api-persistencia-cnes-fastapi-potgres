from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.estabelecimento import Estabelecimento

class EstabelecimentoRepository(BaseRepository[Estabelecimento]):
    def __init__(self, session):
        super().__init__(session, Estabelecimento)

    async def create(self, data: dict) -> Estabelecimento:
        try:
            # Create entity
            entity = self.model(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            
            # Get fresh copy with relationships
            query = select(self.model).options(
                selectinload(self.model.endereco)
            ).where(self.model.id == entity.id)
            result = await self.session.execute(query)
            return result.scalar_one()
            
        except IntegrityError as e:
            await self.session.rollback()
            if 'estabelecimentos_codigo_unidade_key' in str(e):
                raise HTTPException(status_code=400, detail="Código da unidade já existe")
            if 'estabelecimentos_codigo_cnes_key' in str(e):
                raise HTTPException(status_code=400, detail="Código CNES já existe")
            raise HTTPException(status_code=400, detail="Erro ao criar estabelecimento")

    async def update(self, id: int, data: dict) -> Estabelecimento | None:
        try:
            query = update(self.model).where(
                self.model.id == id
            ).values(**data).returning(self.model)
            result = await self.session.execute(query)
            await self.session.flush()
            
            # Get fresh copy with relationships
            entity = result.scalar_one_or_none()
            if entity:
                query = select(self.model).options(
                    selectinload(self.model.endereco)
                ).where(self.model.id == id)
                result = await self.session.execute(query)
                return result.scalar_one()
            return None
            
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Erro ao atualizar estabelecimento")

    async def get_all_with_endereco(self) -> list[Estabelecimento]:
        query = select(self.model).options(selectinload(self.model.endereco))
        result = await self.session.execute(query)
        return list(result.scalars().unique())
    
    async def get_by_id_with_endereco(self, id: int) -> Estabelecimento | None:
        query = select(self.model).options(selectinload(self.model.endereco)).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_unidade(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_unidade == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_codigo_cnes(self, codigo: str) -> Estabelecimento | None:
        query = select(self.model).where(self.model.codigo_cnes == codigo)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
