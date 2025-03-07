from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.equipeprof import EquipeProf

class Profissional(BaseModel):
    __tablename__ = "profissionais"

    codigo_profissional_sus = Column(String, nullable=False, unique=True)
    nome_profissional = Column(String, nullable=False)
    codigo_cns = Column(String, nullable=False)
    situacao_profissional_cadsus = Column(String, nullable=False)

    equipes = relationship("Equipe", secondary="equipeprofs", back_populates="profissionais", lazy='selectin')

