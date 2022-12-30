import pandas as pd
import pyarrow as pa
from app.src.helpers import _abrir_caminho_diretorio


def gerar_parquet(arquivo: str, df: list):
    """
    Gerar um arquivo parquet compactado a partir de uma lista de dicionários.
    é necessário ter os pacotes pandas e pyarrow 
    """
    dataframe = pd.DataFrame.from_records(df)

    arquivo = arquivo+".gzip"
    _abrir_caminho_diretorio(arquivo)

    dataframe.to_parquet(arquivo, compression="gzip")
    # print(dataframe.head())