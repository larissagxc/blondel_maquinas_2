from typing import Dict, Tuple
import os
import csv

class Dados:
    """Classe abstrata para lidar com funções de utilidades (e.g. ler arquivos, validar dados...)"""

    @staticmethod
    def ler_dados(nome_arquivo : str, separador: str = ",") -> Dict[str, str]:
        """
        Função estática que lida com o acesso ao arquivo de entrada e ingere os dados
        """
        if not os.path.isfile(nome_arquivo):
            print (f"Arquivo '{nome_arquivo}' Não existe sob {os.getcwd()}. Retornando dicionário vazio")
            return {}
        else:
            with open(nome_arquivo, 'r') as arq:
                dados = {}
                linhas = csv.reader(arq, delimiter=separador)
                for linha in linhas:
                    # Ignorar linha de cabeçalho/comentário
                    if linha[0].startswith('#'):
                        continue
                    # Atribui o primeiro campo como chave e o segundo como valor
                    dados[linha[0].strip()] = linha[1].strip()
            return dados
        
    @staticmethod
    def validar_dados(dados: Dict[str, str]) -> Tuple[bool, str]:
        """
        Valida a entrada de dados com 3 critérios:
            1. Todos os dados necessários providos no arquivo existem;
            2. É do tipo aceito (float)
            3. É positivo
        """
        variaveis_esperadas = ['Ua', 'S','f','Xd','Xq','Ra','P_mec']
        # Compara se a lista de variáveis recebidas contem pelo menos as variáveis esperadas e se têm o nome certo.
        if not set(variaveis_esperadas).issubset(dados.keys()):
            return False, f"Variável com nome incorreto ou faltante.", f"Variáveis esperadas: {variaveis_esperadas}", f"Recebidas: {list(dados.keys())}"

        for chave, valor in dados.items():
        # Tenta converter o valor para float para cada valor convertido
            try: 
                valor_f = float(valor)
                if valor_f <= 0:
                    return False, f"Valor de {chave} ({valor}) não é maior que zero."
            # Retorna um erro de tipo (pois não conseguiu converter para número)
            except ValueError:
                return False, f"Valor de {chave} ({valor}) não é numérico."
        # Retorna True se os dados são válidos
        return True, "Dicionário válido"