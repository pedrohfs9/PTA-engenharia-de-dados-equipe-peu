import pandas as pd
import unicodedata
import numpy as np
from datetime import datetime

# FUNÇÕES GENERICAS
def converter_para_float(df: pd.DataFrame, colunas: list):
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '.', regex=False), 
                errors='coerce'
            )
    return df

def tratar_nulos_mediana(df: pd.DataFrame, colunas: list):
    for col in colunas:
        if col in df.columns:
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)
    return df

def tratar_data(df: pd.DataFrame, colunas: list):
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def padronizar_texto(df: pd.DataFrame, colunas: list) -> pd.DataFrame:

    # Remove acentos, converte para MAIÚSCULO e remove espaços nas pontas.
    # Ex: '  São Paulo ' -> 'SAO PAULO'

    def _limpar(texto):
        if pd.isna(texto): return ""
        # Separa o acento da letra
        nfkd = unicodedata.normalize('NFKD', str(texto))
        # Filtra apenas caracteres sem acento
        sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return sem_acento.upper().strip()

    for col in colunas:
        if col in df.columns:
            df[col] = df[col].apply(_limpar)
    return df

# FUNÇÃO E
def processar_dataset_pedidos(dados_brutos: list) -> list:
    """
    Recebe uma lista de dicionários, processa via Pandas e retorna lista de dicionários.
    Agora retorna objetos nativos (datetime, float) para o Pydantic validar.
    """
    
    df = pd.DataFrame(dados_brutos)
    
    if df.empty:
        return []

    # 1. Converter datas
    cols_temporais = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in cols_temporais:
        if col in df.columns:
            # errors='coerce' gera NaT (Not a Time) para erros
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 2. Padronizar status
    if 'order_status' in df.columns:
        df['order_status'] = df['order_status'].astype(str).str.lower().str.strip()
        mapa_status = {
            'delivered': 'entregue', 'invoiced': 'faturado', 'shipped': 'enviado',
            'processing': 'em processamento', 'unavailable': 'indisponível',
            'canceled': 'cancelado', 'created': 'criado', 'approved': 'aprovado'
        }
        df['order_status'] = df['order_status'].replace(mapa_status)

    # 3. Métricas
    cols_req = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    if all(c in df.columns for c in cols_req):
        df['tempo_entrega_dias'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
        df['tempo_entrega_estimado_dias'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.days
        df['diferenca_entrega_dias'] = df['tempo_entrega_dias'] - df['tempo_entrega_estimado_dias']
        
        condicoes = [
            df['order_delivered_customer_date'].isna(),
            df['diferenca_entrega_dias'] <= 0,
            df['diferenca_entrega_dias'] > 0
        ]
        valores = ['Não Entregue', 'Sim', 'Não']
        df['entrega_no_prazo'] = np.select(condicoes, valores, default='Indefinido')

    # 4. Substituir NaN por None para compatibilidade com Pydantic
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient='records')