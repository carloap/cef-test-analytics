# ms_analytics
Estudo para aplicar modelos probabilísticos e padrões coincidêntes para determinar um possível resultado dentro de uma série histórica de sorteios divulgados na CEF BR

### Virtual Environment
#### Ambiente virtual controlado em python

```Shell
python3 -m venv venv 
. venv/bin/activate 
pip3 install -r requeriments.txt 
```

### Execução
#### Extração dos dados
O script irá fazer uma requisição inicial para obter um parâmetro exclusivo do cabeçalho, montar uma URL e então consulta-la. 
Caso haja alguma interrupção, ele continuará de onde parou.

OBS: O próprio portal dispõe de dump de dados, porém em um formato <s>inortodoxo</s> HTML, onde é necessário um módulo "web-scraping" para extraí-los das respectivas tags. Por tanto, desconsiderei seu uso para adotar a ATEP (<b>A</b>dequação <b>T</b>écnica <b>E</b>mergencial <b>P</b>ermanente).
> Coletar os dados retroativos de todos os sorteios, do mais recente até o primeiro de 1996.

```Shell
python3 extract.py 
```

#### Transformação dos dados
TODO: ler arquivo final e montar o dicionário só com as informações que interessam
