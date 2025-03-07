from pydantic import BaseModel, Field

class ProfissionalBase(BaseModel):
    codigo_profissional_sus: str = Field(
        example="123456",
        min_length=1,
        max_length=20,
        description="Código único do profissional"
    )
    nome_profissional: str = Field(
        example="Dr. Fulano de Tal",
        min_length=3,
        max_length=255,
        description="Nome do profissional"
    )
    codigo_cns: str = Field(
        example="123456",
        min_length=1,
        max_length=20,
        description="Código do CNS"
    )
    situacao_profissional_cadsus: str = Field(
        example="Ativo",
        min_length=1,
        max_length=20,
        description="Situação do profissional no CadSUS"
    )

class ProfissionalCreate(ProfissionalBase):
    pass

class Profissional(ProfissionalBase):
    id: int = Field(
        example=1,
        description="ID do profissional"
    )

    class Config:
        from_attributes = True