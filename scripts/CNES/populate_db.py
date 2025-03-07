import pandas as pd
import asyncio
from datetime import datetime
from typing import Dict, List
import os
from fastapi import HTTPException
from core.database import get_direct_session, init_models
from repositories.equipe import EquipeRepository
from repositories.equipeprofs import EquipeProfRepository
from repositories.mantenedora import MantenedoraRepository
from repositories.estabelecimento import EstabelecimentoRepository
from repositories.endereco import EnderecoRepository
from repositories.profissional import ProfissionalRepository

def read_csv_file(file_path: str) -> List[Dict]:
    return pd.read_csv(file_path, sep=';', dtype="str", encoding='latin1', lineterminator="\n").to_dict(orient='records')

async def create_mantenedora(repo: MantenedoraRepository, data: Dict) -> Dict:
    try:
        date_str = data["TO_CHAR(DT_PREENCHIMENTO,'DD/MM/YYYY')"]
        if date_str:
            try:
                created_date = datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                created_date = None
        else:
            created_date = None

        print("\n\n")
        print(data)
        print("\n\n")
        mantenedora = {
            "cnpj_mantenedora": str(data["NU_CNPJ_MANTENEDORA"]),
            "nome_razao_social_mantenedora": str(data["NO_RAZAO_SOCIAL"]),
            "numero_telefone_mantenedora": str(data["NU_TELEFONE"]),
            "codigo_banco": str(data["CO_BANCO"]),
            "numero_agencia": str(data["NU_AGENCIA"]), 
            "numero_conta_corrente": str(data["NU_CONTA_CORRENTE"]),
            "data_criacao_mantenedora": created_date
        }

        return await repo.create(mantenedora)
    except Exception as e:
        print(f"Error creating mantenedora: {str(e)}")
        return None

async def create_estabelecimento_with_endereco(
    estab_repo: EstabelecimentoRepository,
    end_repo: EnderecoRepository,
    estab_data: Dict,
    mant_data: Dict
) -> Dict:
    try:
        estabelecimento = {
            "codigo_unidade": str(estab_data["CO_UNIDADE"]),
            "codigo_cnes": str(estab_data["CO_CNES"]),
            "cnpj_mantenedora": str(mant_data["NU_CNPJ_MANTENEDORA"]),
            "nome_razao_social_estabelecimento": str(estab_data["NO_RAZAO_SOCIAL"]),
            "nome_fantasia_estabelecimento": str(estab_data["NO_FANTASIA"]),
            "numero_telefone_estabelecimento": str(estab_data["NU_TELEFONE"]),
            "email_estabelecimento": str(estab_data.get("NO_EMAIL"))
        }

        try:
            estab_result = await estab_repo.create(estabelecimento)
            if not estab_result:
                print(f"Error creating estabelecimento: {estabelecimento['codigo_unidade']}")
                return None

            # Convert latitude and longitude to float
            latitude = str(estab_data.get("NU_LATITUDE")) if str(estab_data.get("NU_LATITUDE")) else ""
            longitude = str(estab_data.get("NU_LONGITUDE")) if str(estab_data.get("NU_LONGITUDE")) else ""

            endereco = {
                "estabelecimento_id": estab_result.id,
                "latitude": latitude,
                "longitude": longitude,
                "cep_estabelecimento": str(estab_data["CO_CEP"]),
                "bairro": str(estab_data["NO_BAIRRO"]),
                "logradouro": str(estab_data["NO_LOGRADOURO"]),
                "numero": str(estab_data["NU_ENDERECO"]),
                "complemento": str(estab_data["NO_COMPLEMENTO"])
            }

            await end_repo.create(endereco)
            return estab_result

        except ValueError as ve:
            print(f"Error converting coordinates: {str(ve)}")
            return None
        except HTTPException as he:
            print(f"HTTP Error: {he.detail}")
            return None

    except Exception as e:
        print(f"Error processing estabelecimento: {str(e)}")
        return None

async def create_equipe(eqipe_repo: EquipeRepository, data: Dict) -> Dict:
    try:
        print(data)
        equipe = {
            "codigo_equipe": str(data["SEQ_EQUIPE"]),
            "nome_equipe": data["NO_USUARIO"],
            "tipo_equipe": str(data["TP_EQUIPE"]),
            "codigo_unidade": str(data["CO_UNIDADE"])
        }

        return await eqipe_repo.create(equipe)
    except Exception as e:
        print(f"Error creating equipe: {str(e)}")
        return None

async def create_profissional(profRepo: ProfissionalRepository, data: Dict) -> Dict:
    try:
        profissional = {
            "codigo_profissional_sus": str(data["CO_PROFISSIONAL_SUS"]),
            "nome_profissional": data["NO_PROFISSIONAL"],
            "codigo_cns": str(data["CO_CNS"]),
            "situacao_profissional_cadsus": str(data["ST_NMPROF_CADSUS"]),
        }

        return await profRepo.create(profissional)
    except Exception as e:
        print(f"Error creating profissional: {str(e)}")
        return None

async def create_equipe_profissional(repo: EquipeProfRepository, data: Dict) -> Dict:
    try:
        equipe_profissional = {
            "codigo_equipe": str(data["SEQ_EQUIPE"]),
            "codigo_profissional_sus": str(data["CO_PROFISSIONAL_SUS"])
        }

        return await repo.create(equipe_profissional)
    except Exception as e:
        print(f"Error creating equipe profissional: {str(e)}")
        return None

async def main():
    await init_models()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mantenedoras = read_csv_file(os.path.join(current_dir, 'tbMantenedora202501.csv'))
    estabelecimentos = read_csv_file(os.path.join(current_dir, 'tbEstabelecimento202501.csv'))
    equipes = read_csv_file(os.path.join(current_dir, 'tbEquipe.csv'))
    profissionais = read_csv_file(os.path.join(current_dir, 'tbProf.csv'))
    equipeprofs = read_csv_file(os.path.join(current_dir, 'tbEquipeProf.csv'))
    
    async with await get_direct_session() as session:
        mant_repo = MantenedoraRepository(session)
        estab_repo = EstabelecimentoRepository(session)
        end_repo = EnderecoRepository(session)
        prof_repo = ProfissionalRepository(session)
        eqprof_repo = EquipeProfRepository(session)
        eq_repo = EquipeRepository(session)

        for mant in mantenedoras:
            await create_mantenedora(mant_repo, mant)
        
        for estab in estabelecimentos:
            mant = next((m for m in mantenedoras if (m["NU_CNPJ_MANTENEDORA"]) == (estab["NU_CNPJ_MANTENEDORA"])), None)
            
            if not mant:
                print(f"Warning: Mantenedora not found for estabelecimento {estab['CO_UNIDADE']} with CNPJ {estab['NU_CNPJ_MANTENEDORA']}")
                continue
                
            await create_estabelecimento_with_endereco(estab_repo, end_repo, estab, mant)
        await session.commit()

        for equipe in equipes:
            await create_equipe(eq_repo, equipe)
        await session.commit()

        for prof in profissionais:
            await create_profissional(prof_repo, prof)
        await session.commit()

        for eqprof in equipeprofs:
            await create_equipe_profissional(eqprof_repo, eqprof)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
