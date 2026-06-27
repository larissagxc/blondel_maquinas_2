from typing import Dict, Tuple, Union
import os
import csv
from io import StringIO

class Dados:
    def __init__(self, fonte: Union[str, StringIO], separador: str = ","):
        self.dados = self._ler_dados(fonte, separador)
        self.dados_brutos = self._ler_brutos(fonte)

    @staticmethod
    def _ler_dados(fonte: Union[str, StringIO], separador: str = ",") -> Dict[str, str]:
        """
        Lê os dados 
        """
        if isinstance(fonte, str):
            if not os.path.isfile(fonte):
                print(f"Arquivo '{fonte}' Não existe sob {os.getcwd()}. Retornando dicionário vazio")
                return {}
            arq = open(fonte, 'r')
        else:
            arq = fonte

        dados = {}
        linhas = csv.reader(arq, delimiter=separador)
        for linha in linhas:
            if linha[0].startswith('#'):
                continue
            dados[linha[0].strip()] = linha[1].strip()
        if isinstance(fonte, str):
            arq.close()
        return dados

    @staticmethod
    def _ler_brutos(fonte: Union[str, StringIO]) -> str:
        if isinstance(fonte, str):
            with open(fonte) as arq:
                return arq.read()
        return fonte.getvalue()

    def validar(self) -> Tuple[bool, str]:
        variaveis_esperadas = ['Ua', 'S', 'f', 'Xd', 'Xq', 'Ra', 'P_mec']
        if not set(variaveis_esperadas).issubset(self.dados.keys()):
            return False, (f"Variável com nome incorreto ou faltante. "
                           f"Variáveis esperadas: {variaveis_esperadas}. "
                           f"Recebidas: {list(self.dados.keys())}")
        for chave, valor in self.dados.items():
            try:
                valor_f = float(valor)
                if valor_f <= 0:
                    return False, f"Valor de {chave} ({valor}) não é maior que zero."
            except ValueError:
                return False, f"Valor de {chave} ({valor}) não é numérico."
        return True, "Dicionário válido"