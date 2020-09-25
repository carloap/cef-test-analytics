import requests
import json
import time
import os
from pathlib import Path

from util.MySymmetricCrypto import MySymmetricCrypto as MSCrypto

# Chave usada para criptografia de dados
_SECRET_KEY_ = b'w1AiyQf_5A_GBbTaPcLC5vKpyLwXj-FkMtsJxE8XoQI='
scrypto = MSCrypto(_SECRET_KEY_)


# Parâmetros criptografados
VAR_ENDPOINT_ENCRYPTED = b'gAAAAABfObL3-CzTP3DHLVBSkrMx56BWuCqRU394ptGyYV8Adebc5ivr5LrxcsGsdt6cJ4fItsz_ZXxS2UX_N4rRBIwcCIRmfczYgZZhhLwqV4Jvo1DLOmg='
VAR_URI_START_ENCRYPTED = b'gAAAAABfObSD-1FzQUWoxFfRRk-1Ows0FCpJql1DSqgRNQFEN5CayUuPdgsBPI2GyFKJUo3Urt0BiIHCCaSZeTSjSPt-EIL7lGY2o5qUfczErhmICpDP7IHominqSrTj02-nKwQnsddR'
VAR_URI_SUFFIX_ENCRYPTED = b'gAAAAABfObOlrfv-VqbPFylBFb-Te8Lv18-E4S3A9pc_DfS8NSXfh7-dN7WwzSjyN5J2Df9gV2eRJUPiruMa82W8hBJHOApanYCf13DfkG0AojvUsfgfg0pOevirK41ehKGIbQXENDmhoTrQLoZ2BnsEFOfm4TXH1-B_BUybxIBCDYqf22HQOF5YQkIX8dEv2HNvYpRKJwGu'


# Parâmetros de URL
VAR_ENDPOINT = scrypto.decrypt(msg=VAR_ENDPOINT_ENCRYPTED).decode() 
VAR_URI_START = scrypto.decrypt(msg=VAR_URI_START_ENCRYPTED).decode() 
VAR_URI_SUFFIX = scrypto.decrypt(msg=VAR_URI_SUFFIX_ENCRYPTED).decode() + str(time.time()).replace('.','')[0:13]
VAR_URI_PATH_PARAM = ""


# Arquivos de cache
dict_cache_files = {
    'URIPARAM_FILE': 'cache/_cache_uri_param.txt',
    'IDCONCURSO_FILE': 'cache/_cache_idconcurso_pos.txt'
}

# Arquivos de resultados
dict_source_files = {
    'SOURCE_CONTEST_FILE': 'bucket/contest_results.raw'
}


# Manipula em um arquivo de cache, o retorno da primeira requisição contendo a URI codificada para consumir a API de buscas
def defineCacheParam(filename_cache, callback_func, force_cache=False):
    # Cria a arvore de diretórios
    filesys_path = Path('/'.join(filename_cache.split('/')[0:-1]))
    filesys_path.mkdir(parents=True, exist_ok=True)

    file = filename_cache
    if os.path.exists(file) and force_cache is not True :
        print(' lendo cache... ' + filename_cache)
        with open(file, 'rb') as reader:
            resp = reader.read()
            resp = scrypto.decrypt(resp).decode()
            return resp
    else:
        result = callback_func
        with open(file, 'wb') as out_file:
            out_file.write( scrypto.encrypt(result.encode()) )
            return result


# Escreve um arquivo, linha a linha
def writeFile(filename, dict_content):
    # Cria a arvore de diretórios
    filesys_path = Path('/'.join(filename.split('/')[0:-1]))
    filesys_path.mkdir(parents=True, exist_ok=True)

    with open(filename, 'a') as out_file:
        json.dump(dict_content, out_file)
        out_file.write(os.linesep)


# Tenta efetuar a primeira requisição para obter a URI codificada para consultas na API
def getUriParam():
    cookies = {'security': 'true'}
    url = VAR_ENDPOINT + VAR_URI_START

    response = requests.post(url, cookies=cookies)
    dict_resp = response.headers
    if dict_resp is not None and 'Content-Location' in dict_resp:
        return dict_resp['Content-Location']
    else:
        print('Tentando novamente, aguarde!')
        time.sleep(5) # Aguardando para tentar novamente
        getUriParam()


# Obtem o resultado do consurso consultado e armazena o 'dado bruto em um arquivo'
def getContestResult(url):
    # Tenta carregar o ID do concurso de onde parou antes, ou cacheia o primeiro registro
    savepoint_idConcurso = defineCacheParam(filename_cache=dict_cache_files['IDCONCURSO_FILE'], callback_func='')

    idConcursoParam = ''
    if savepoint_idConcurso is not '':
        print(' savepoint: ' + str(savepoint_idConcurso))
        idConcursoParam = '&concurso=' + str(savepoint_idConcurso)

    # primeira requisição
    response = requests.get(url + idConcursoParam)
    if response.status_code == 200:
        dict_resp = response.json()
        idConcursoAnterior = dict_resp['concursoAnterior'] if 'concursoAnterior' in dict_resp else None
        defineCacheParam(filename_cache=dict_cache_files['IDCONCURSO_FILE'], callback_func=str(idConcursoAnterior), force_cache=True) # savepoint
        writeFile(dict_source_files['SOURCE_CONTEST_FILE'], dict_resp) # Escreve o primeiro objeto em um arquivo

        # Iterar, consultar e guardar o resultado
        for c in range(int(dict_resp['concurso'])-1, 0, -1):
            # iterando requisições

            response = requests.get(url + '&concurso=' + str(c))
            if response.status_code == 200:
                dict_resp = response.json()
                _idConcursoAnterior = dict_resp['concursoAnterior'] if 'concursoAnterior' in dict_resp else None
                defineCacheParam(filename_cache=dict_cache_files['IDCONCURSO_FILE'], callback_func=str(_idConcursoAnterior), force_cache=True) # savepoint
                writeFile(dict_source_files['SOURCE_CONTEST_FILE'], dict_resp) # Escreve os dicts linha a linha

                print('concurso = ' + str(dict_resp['concurso']))

                time.sleep(2) # pause
            else: 
                print(' consulta ao sorteio falhou, aguardando para tentar novamente...')
                time.sleep(5) # pause
                getContestResult(url) # recursão se necessário

        if c >= 1:
            print('Fim')
            os.remove(dict_cache_files['URIPARAM_FILE'])
            os.remove(dict_cache_files['IDCONCURSO_FILE'])

    else:
        print(' consulta do sorteio mal-sucedida!')
        print('tentando novamente, aguarde...')
        time.sleep(3) # pause
        getContestResult(url) # recursão se necessário


# Executor
if __name__ == "__main__":
    # Obtém ou cria um cache com a URI consultar os resultados no Endpoint
    VAR_URI_PATH_PARAM = defineCacheParam(filename_cache=dict_cache_files['URIPARAM_FILE'], callback_func=getUriParam())

    # Coleta novos dados e guarda em arquivo
    getContestResult( url=(VAR_ENDPOINT + VAR_URI_PATH_PARAM + VAR_URI_SUFFIX) )
    
