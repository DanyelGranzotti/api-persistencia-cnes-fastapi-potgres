# API de Dados do Sistema de Saúde Brasileiro

## Sobre o Projeto
API REST para gerenciamento de dados do Cadastro Nacional de Estabelecimentos de Saúde (CNES/DataSUS), desenvolvida como parte da disciplina de Persistência de Dados.

## Tecnologias
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Python 3.8+

## Configuração do Ambiente

### Pré-requisitos
- Docker e Docker Compose
- Python 3.8 ou superior
- Git

### Instalação

1. Clone e configure o projeto:
```bash
git clone https://github.com/DanyelGranzotti/api-persistencia-cnes-fastapi-potgres.git
cd api-persistencia-cnes-fastapi-potgres
pip install -r requirements.txt
```

2. Inicie o banco de dados:
```bash
docker-compose up -d
```

4. Execute as migrações:
```bash
alembic upgrade head
```

5. Inicie a aplicação:
```bash
uvicorn main:app --reload
```

### População do Banco de Dados

Para popular o banco de dados com dados iniciais do CNES, execute:

```bash
python -m scripts.CNES.populate_db
```

> **Nota**: Este processo pode levar alguns minutos dependendo do volume de dados.

## Documentação da API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Desenvolvimento

### Criar Nova Migração
```bash
alembic revision --autogenerate -m "descrição"
```
### Aplicar Migrações
```bash
alembic upgrade head
```

 python -m scripts.CNES.populate_db