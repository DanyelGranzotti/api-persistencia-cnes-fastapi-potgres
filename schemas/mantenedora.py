from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class MantenedoraBase(BaseModel):
    cnpj_mantenedora: str = Field(
        example="12345678901234",
        min_length=14,
        max_length=14,
        description="CNPJ da mantenedora"
    )
    nome_razao_social_mantenedora: str = Field(
        example="Mantenedora LTDA",
        min_length=3,
        max_length=255,
        description="Razão social da mantenedora"
    )
    numero_telefone_mantenedora: str | None = Field(
        default=None,
        example="(85) 3219-1234",
        max_length=20,
        description="Número de telefone da mantenedora"
    )
    codigo_banco: str | None = Field(
        default=None,
        example="001",
        min_length=3,
        max_length=3,
        description="Código do banco"
    )
    numero_agencia: str | None = Field(
        default=None,
        example="1234",
        max_length=10,
        description="Número da agência"
    )
    numero_conta_corrente: str | None = Field(
        default=None,
        example="123456-7",
        max_length=20,
        description="Número da conta corrente"
    )

    @field_validator('cnpj_mantenedora')
    def validate_cnpj(cls, v):
        if not v.isdigit():
            raise ValueError('CNPJ deve conter apenas números')
        if len(v) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        return v

    @field_validator('numero_telefone_mantenedora')
    def validate_telefone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, v))
        # Format the number
        if len(digits) in [10, 11]:
            return f"({digits[:2]}) {digits[2:-4]}-{digits[-4:]}"
        return v

class MantenedoraCreate(MantenedoraBase):
    pass

class MantenedoraUpdate(MantenedoraBase):
    pass

class Mantenedora(MantenedoraBase):
    id: int
    data_criacao_mantenedora: datetime

    class Config:
        from_attributes = True
