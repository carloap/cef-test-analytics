from invoke import task
from app.src.extrair import MegaSena as Mega
from app.src.helpers import set_logger

logger = set_logger("loterias")


@task
def hello(c, name="There"):
    """
    Task de teste
    """
    c.run("echo 'Hello {}'".format(name))

@task
def help(c):
    """
    Task de ajuda para comandos válidos
    """
    logger.info("Tarefas válidas ")
    import tasks as tsks
    lista_funcoes = dir(tsks)
    lista_funcoes = list( filter(lambda f: f[:2] not in "__" and f not in ['task','help'], lista_funcoes) )
    logger.info(lista_funcoes)

@task
def extrairMegaSena(c):
    """
    Task para coletar dados dos sorteios da MegaSena
    """
    logger.info("Extraindo dados da MegaSena da API de loterias da caixa")
    ms = Mega()

    posicao = ms.valida_ultima_leitura()
    resp = ms.ler_concurso(posicao) # 0 == ler a partir do último

    while ms.posicao_concurso > ms.posicao_concurso_limite:
        posicao = ms.posicao_concurso - 1 # Lê a ultima posição na memória
        resp2 = ms.ler_concurso(posicao)
    
    logger.info("Extração finalizada") 
