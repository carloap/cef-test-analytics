import os
import sys
import logging
from pathlib import Path


def set_logger(context: str = "logger"):
    """
    Define um novo contexto de logging do python 
    """
    # Log formatter
    formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s :: %(message)s :: %(pathname)s:%(lineno)s' # noqa E501
    )
    # Handler to print
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    # Log object
    logger = logging.getLogger(context)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def ler_arquivo(arquivo):
    """
    Função para leitura de arquivos de texto
    """
    if os.path.isfile(arquivo):
        with open(arquivo, 'r', encoding='utf8') as objeto:
            return objeto.read()
    return None

def escrever_arquivo(arquivo, conteudo):
    """
    Função para escrita de arquivo de texto
    """
    caminho_arquivo = Path('/'.join(arquivo.split('/')[0:-1]))
    caminho_arquivo.mkdir(parents=True, exist_ok=True)
    with open(arquivo, 'a', encoding='utf8') as saida_arquivo:
        saida_arquivo.write(conteudo)

def remover_arquivo(arquivo):
    """
    Função para exclusão de arquivos
    """
    if os.path.exists(arquivo):
        os.remove(arquivo)