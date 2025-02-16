from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Estabelecimento(BaseModel):
    __tablename__ = "estabelecimentos"

    codigo_unidade = Column(String(20), nullable=False, unique=True)
    codigo_cnes = Column(String(20), nullable=False, unique=True)
    cnpj_mantenedora = Column(String(14), nullable=False)
    nome_razao_social_estabelecimento = Column(String(255), nullable=False)
    nome_fantasia_estabelecimento = Column(String(255), nullable=False)
    numero_telefone_estabelecimento = Column(String(20))
    email_estabelecimento = Column(String(255))
    endereco = relationship("Endereco", back_populates="estabelecimento", uselist=False)
