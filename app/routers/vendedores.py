from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

from ..schemas.data_models import Vendedores_bruto, Vendedores_processado
from ..services.tools import padronizar_texto

router = APIRouter(tags=["Vendedores"])

@router.post("/processar/vendedores", response_model=List[Vendedores_processado])
async def processar_vendedores(dados: List[Vendedores_bruto]):
    # Recebe dados brutos de vendedores, padroniza texto e valida tipos.

    try:

        df = pd.DataFrame([d.model_dump() for d in dados])
        
        if df.empty:
            return []

        # Padronização de Texto
        # Requisito: seller_city (sem acento, upper) e seller_state (upper)
        df = padronizar_texto(df, ['seller_city', 'seller_state'])

        # Garantia de Tipagem
        # O schema de saída exige que o CEP seja string. Garantimos isso aqui. (Não foi cobrado no desafio mas decidi adicionar)
        if 'seller_zip_code_prefix' in df.columns:
            df['seller_zip_code_prefix'] = df['seller_zip_code_prefix'].astype(str)

        # Retorno
        # O FastAPI/Pydantic fará a validação final contra o modelo Vendedores_processado
        return df.to_dict(orient='records')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar vendedores: {str(e)}")