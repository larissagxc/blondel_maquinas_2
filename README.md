## Trabalho de Máquinas 2: Diagrama de Blondel de um motor de polos salientes

O presente trabalho contempla:
* a leitura e manipulação de dados de um arquivo externo;
* cálculos para motor e gerador síncrono;
* diagrama de Blondel.

### Codagem colaborativa via Github

#### Setup Inicial: ambiente python e bibliotecas

1. Instalar o ambiente virtual python (`sudo apt update && sudo apt install python3-venv`)
2. Criar um ambiente virtual no terminal Linux: `python3 -m venv <nome do ambiente>` 
    1. Exemplo: `python3 -m venv virtualenv` 
3. Ativar o ambiente virtual: `source virtualenv/bin/activate`
4. Agora com o ambiente ativo, é possível instalar os pacotes com pip a partir de `requirements.txt: `pip install -r requirements.txt`
5. Para rodar a interface: `streamlit run src/interface.py`
    1. Aparecerá um link no terminal com o endereço local para executar o app.
