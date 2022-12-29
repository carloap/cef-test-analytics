# cef-test-analytics

Projeto simples (refatorado) de coleta de dados das loterias da CEF BR, e análise exploratória.

## Ambiente virtual em Python

```Shell
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r app/requeriments.txt
```

## Execução

```Shell
invoke extrairMegaSena
```

Esse script é executado em terminal, e vai coletar os dados referentes aos sorteios realizados na megasena, e armazenar em arquivo seu resultado e sua última posição lida, para casos de interrupções.


## TODO: análise exploratória