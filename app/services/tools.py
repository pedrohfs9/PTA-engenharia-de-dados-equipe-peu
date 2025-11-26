import pandas as pd
import unicodedata
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