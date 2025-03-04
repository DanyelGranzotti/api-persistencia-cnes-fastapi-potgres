from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Endereco(BaseModel):
    __tablename__ = "enderecos"

    estabelecimento_id = Column(Integer, ForeignKey("estabelecimentos.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(String, nullable=True)  # Changed from String to Float
    longitude = Column(String, nullable=True)  # Changed from String to Float
    cep_estabelecimento = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=True)
    complemento = Column(String, nullable=True)

    estabelecimento = relationship("Estabelecimento", back_populates="endereco")
