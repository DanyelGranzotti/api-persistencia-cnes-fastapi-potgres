from pydantic import BaseModel, Field

from schemas.profissional import Profissional

class EquipeBase(BaseModel):
    codigo_equipe: str = Field(
        example="123456",
        min_length=1,
        max_length=20,
        description="Código único da equipe"
    )
    nome_equipe: str = Field(
        example="Equipe de Saúde da Família",
        min_length=3,
        max_length=255,
        description="Nome da equipe"
    )
    tipo_equipe: str = Field(
        example="ESF",
        min_length=1,
        max_length=20,
        description="Tipo da equipe"
    )
    codigo_unidade: str = Field(
        example="123456",
        min_length=1,
        max_length=20,
        description="Código da unidade"
    )
    estabelecimento_id: int = Field(
        example=1,
        description="ID do estabelecimento"
    )

class EquipeCreate(EquipeBase):
    pass

class Equipe(EquipeBase):
    id: int = Field(
        example=1,
        description="ID da equipe"
    )

    profissionais: list[Profissional] = Field(
        example=[],
        description="Lista de profissionais da equipe"
    )

    class Config:
        from_attributes = True
