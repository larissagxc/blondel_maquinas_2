from typing import Dict

class Maquina():
    
    dados: Dict = {}
    "Dicionário que armazena todos os dados de placa da máquina"
    
    dados_r: Dict = {}
    "Dicionário que armazena todos os dados reais da máquina, visto que os dados de placa podem ser modificados"



    def __init__(self, dados: Dict, verboso: bool = True):

        self.dados = dados
        self.dados_r = self.dados

        if verboso:
            print("Máquina inicializada. Parâmetros:")
            # TODO: Adicionar print dos parÂmetros