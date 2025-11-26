from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

from ..schemas.data_models import Itensdepedidos_bruto, Itensdepedidos_processado
from ..services.tools import converter_para_float, tratar_nulos_mediana, tratar_data

router = APIRouter(tags=["Itens de Pedidos"])

@router.post("/processar/itens_pedidos", response_model=List[Itensdepedidos_processado])
async def processar_itens_pedidos(dados: List[Itensdepedidos_bruto]):
    # Recebe itens de pedidos, trata nulos (mediana), converte tipos e datas.

    try:
        df = pd.DataFrame([d.model_dump() for d in dados])

        if df.empty:
            return []

        # Conversão Numérica
        # Garante que price e freight_value sejam float (troca vírgula por ponto se necessário)
        df = converter_para_float(df, ['price', 'freight_value'])

        # Tratamento de Nulos
        # Preenche nulos em price e freight_value com a mediana
        df = tratar_nulos_mediana(df, ['price', 'freight_value'])

        # Datas
        # Converte shipping_limit_date para datetime/timestamp
        df = tratar_data(df, ['shipping_limit_date'])
        
        # Extra: como o modelo cobra o retorno de todos os valores datetime para a data
        # adicionei um valor padrão (data muito antiga) caso a função acima retorne NaT.
        df['shipping_limit_date'] = df['shipping_limit_date'].fillna(pd.Timestamp("1900-01-01"))

        # 5. Retorno
        return df.to_dict(orient='records')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar itens de pedidos: {str(e)}")