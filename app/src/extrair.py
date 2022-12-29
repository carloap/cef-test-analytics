import logging
import requests
import json
from app.src.helpers import (
    ler_arquivo, escrever_arquivo, remover_arquivo)

# suppress warnings
requests.packages.urllib3.disable_warnings() 


class MegaSena:


    def __init__(self):
        self.logger = logging.getLogger("loterias.megasena")

        self._baseurl_ = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/"
        self._headers_ = {
            "Accept": "application/json, text/plain, */*"
        }

        self.posicao_concurso = 0
        self.posicao_concurso_limite = 1000 # o concurso #1000 foi em 30/08/2008; o #2 foi em 11/03/1996
        self.lista_dezenas = []

        self.arquivo_destino_ultima_posicao = "data/staging/megasena/id_posicao.txt"
        self.arquivo_destino_resultados = "data/staging/megasena/resultados.txt"


    def ler_concurso(self, codigo: int):
        """
        Ler e coletar dados em formato json do concurso da megasena.
        Caso o código informado seja zero, será lido o último.
        """
        urlpath = self._baseurl_ + (str(codigo) if codigo > 0 else "")

        resultado = None
        try:
            resposta = requests.get(
                url=urlpath,
                headers=self._headers_,
                verify=False
            )

            if resposta.ok:
                resultado = resposta.json()
                msg = f"Resposta OK: concurso {codigo}"
                self.logger.info(msg)

                self.validar_resultado(resultado)
            else:
                msg = "Sem resposta do servidor"
                resultado = {"msg": msg}
                self.logger.info(msg)
                self.logger.info(resposta)

        except Exception as exc:
            msg = f"Erro durante a requisição: {exc}"
            resultado = {"msg": msg}
            self.logger.error(msg)

        return resultado


    def validar_resultado(self, resultado: dict):
        """
        Valida a resposta da requisição e armazena os dados coletados
        """
        if 'numero' in resultado and 'listaDezenas' in resultado:
            self.posicao_concurso = int(resultado["numero"])
            self.lista_dezenas = resultado["listaDezenas"]

            # Escreve o arquivo com o resultado deste concurso
            str_resultado = json.dumps(resultado)
            escrever_arquivo(self.arquivo_destino_resultados, str_resultado+"\n")

            # Checkpoint: remove para recriar o arquivo com a última posição
            remover_arquivo(self.arquivo_destino_ultima_posicao)
            escrever_arquivo(self.arquivo_destino_ultima_posicao, str(self.posicao_concurso))
        else:
            msg = 'Algo inesperado ocorreu e o json não parece válido'
            raise Exception(msg)


    def valida_ultima_leitura(self):
        """
        Lê a última posição do concurso consultado
        """
        conteudo = ler_arquivo(self.arquivo_destino_ultima_posicao)
        if conteudo:
            return int(conteudo)
        else:
            return 0
