from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

# Imports relativos corretos
from ..schemas.data_models import ProductData, ProductList
from ..services.products_service import tratar_produtos

router = APIRouter()

@router.post("/processar", response_model=List[ProductData])
def processar_produtos_endpoint(payload: List[ProductData]):
    """
    Recebe Lista tipada, processa e retorna Lista tipada.
    """
    try:
        # Converter Pydantic -> DataFrame
        dados_brutos = [p.model_dump() for p in payload]
        df_bruto = pd.DataFrame(dados_brutos)
        
        if df_bruto.empty:
            return []
            
        # Chama o serviço refatorado
        df_limpo = tratar_produtos(df_bruto)
        
        return df_limpo.to_dict(orient='records')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro em produtos: {str(e)}")