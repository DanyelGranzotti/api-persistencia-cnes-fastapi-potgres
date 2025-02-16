from pydantic import BaseModel, Field, field_validator
from schemas.endereco import Endereco
import re

class EstabelecimentoBase(BaseModel):
    codigo_unidade: str = Field(
        example="123456",
        min_length=1,
        max_length=20,
        description="Código único da unidade"
    )
    codigo_cnes: str = Field(
        example="7891011",
        min_length=7,
        max_length=7,
        description="Código CNES do estabelecimento"
    )
    cnpj_mantenedora: str = Field(
        example="12345678901234",
        min_length=14,
        max_length=14,
        description="CNPJ da mantenedora"
    )
    nome_razao_social_estabelecimento: str = Field(
        example="Hospital São José LTDA",
        min_length=3,
        max_length=255,
        description="Razão social do estabelecimento"
    )
    nome_fantasia_estabelecimento: str = Field(
        example="Hospital São José",
        min_length=3,
        max_length=255,
        description="Nome fantasia do estabelecimento"
    )
    numero_telefone_estabelecimento: str | None = Field(
        default=None,
        example="(85) 3219-1234",
        max_length=20,
        description="Número de telefone do estabelecimento"
    )
    email_estabelecimento: str | None = Field(
        default=None,
        example="contato@saojose.com.br",
        max_length=255,
        description="Email do estabelecimento"
    )

    @field_validator('cnpj_mantenedora')
    def validate_cnpj(cls, v):
        if not v.isdigit():
            raise ValueError('CNPJ deve conter apenas números')
        if len(v) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        return v

    @field_validator('numero_telefone_estabelecimento')
    def validate_telefone(cls, v):
        if v is None:
            return v
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, v))
        # Check if we have 10 or 11 digits (with area code)
        if len(digits) not in [10, 11]:
            raise ValueError('Telefone deve ter 10 ou 11 dígitos incluindo DDD')
        
        # Format the number to the standard format
        ddd = digits[:2]
        if len(digits) == 11:  # Mobile number
            number = f'{digits[2:7]}-{digits[7:]}'
        else:  # Landline
            number = f'{digits[2:6]}-{digits[6:]}'
        
        formatted = f'({ddd}) {number}'
        return formatted

    @field_validator('email_estabelecimento')
    def validate_email(cls, v):
        if v is None:
            return v
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(v):
            raise ValueError('Email inválido')
        return v

class EstabelecimentoCreate(EstabelecimentoBase):
    mantenedora_id: int

class EstabelecimentoUpdate(EstabelecimentoBase):
    mantenedora_id: int

class Estabelecimento(EstabelecimentoBase):
    id: int
    mantenedora_id: int
    endereco: Endereco | None = None

    class Config:
        from_attributes = True
