from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Endereco(BaseModel):
    __tablename__ = "enderecos"

    latitude = Column(Float)
    longitude = Column(Float)
    cep_estabelecimento = Column(String(8), nullable=False)
    bairro = Column(String(100), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100))
    estabelecimento_id = Column(Integer, ForeignKey('estabelecimentos.id'), unique=True, nullable=False)
    estabelecimento = relationship("Estabelecimento", back_populates="endereco")
