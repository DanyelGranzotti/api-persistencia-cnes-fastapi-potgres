from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from repositories.base import BaseRepository
from models.endereco import Endereco

class EnderecoRepository(BaseRepository[Endereco]):
    def __init__(self, session):
        super().__init__(session, Endereco)
    
    async def create(self, data: dict) -> Endereco:
        try:
            return await super().create(data)
        except IntegrityError as e:
            if 'enderecos_estabelecimento_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Estabelecimento não encontrado ou já possui um endereço cadastrado"
                )
            raise

    async def update(self, id: int, data: dict) -> Endereco | None:
        try:
            return await super().update(id, data)
        except IntegrityError as e:
            if 'enderecos_estabelecimento_id_fkey' in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Estabelecimento não encontrado ou já possui um endereço cadastrado"
                )
            raise
    
    async def get_by_estabelecimento_id(self, estabelecimento_id: int) -> Endereco | None:
        query = select(self.model).where(self.model.estabelecimento_id == estabelecimento_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
