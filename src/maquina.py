from typing import Dict
import numpy as np

class Maquina():
    
    dados: Dict[str, float] = {}
    "Dicionário que armazena todos os dados de placa da máquina, inseridos via arquivo"
    
    dados_calc: Dict[str, float] = {}
    "Dicionário auxiliar que armazena todos os calculados pela máquina, evitando a constante repetição de cálculos"

    def __init__(self, dados: Dict[str, float], dados_interface, verboso: bool = True):

        self.dados = dados
        self.dados_interface = dados_interface
        self.dados_calc = self.dados_calc

        if verboso:
            print("Máquina inicializada. Parâmetros:")
            print("Dados limpos:", self.dados)
            print("Dados da interface:", self.dados_interface)
            # TODO: Adicionar print dos parÂmetros

    def calc_v_t(self) -> complex:
        """
        Calcula a tensão de fase. Retorna um fasor $\vec{V}_t = V_t + j0$ 
        """
        vt = self.dados['Ua'] / np.sqrt(3)
        return vt
    
    def calc_i_n(self) -> float:
        """
        Calcula a corrente nominal. Retorna um float
        """
        i_n = self.dados['S'] / (np.sqrt(3) * self.dados['Ua'])
        return i_n
    
    def calc_phi(self) -> float:
        """
        Calcula o phi à partir do FP fornecido externamente
        """
        phi = np.arccos(self.dados_interface['fp'])
        return phi
    
    def calc_alpha(self) -> float:
        """
        Calcula o Alpha à partir do FP e da característica do FP (Indutivo, Capacitivo) fornecido externamente
        """
        phi = self.calc_phi()
        alpha = phi

        if phi == 0:
            alpha = 0.0
        elif self.dados_interface['tipo_fp'] == "Indutivo":
            alpha = -phi
        elif self.dados_interface['tipo_fp'] == "Capacitivo":
            alpha = phi

        return alpha
    
    def calc_ia(self) -> complex:
        alpha = self.calc_alpha()
        i_a = np.cos(alpha) + 1j*np.sin(alpha)
        return i_a

    def resultados_maquina(self):

        res = {
            "v_t":            self.calc_v_t(),
            "i_n":            self.calc_i_n(),
            "phi_08":         self.calc_phi(),
            "phi_10":         self.calc_phi(),
            "alpha_ind":      self.calc_alpha(),
            "alpha_cap":      self.calc_alpha(),
            "alpha_uni_c":    self.calc_alpha(),
            "alpha_uni_i":    self.calc_alpha(),
            "i_a":            self.calc_ia()
        }

        v_t           = self.calc_v_t()
        i_n           = self.calc_i_n()
        phi_08        = self.calc_phi()
        phi_10        = self.calc_phi()
        alpha_ind     = self.calc_alpha()
        alpha_cap     = self.calc_alpha()
        alpha_uni_c   = self.calc_alpha()
        alpha_uni_i   = self.calc_alpha()
        i_a           = self.calc_ia()

        print(f"v_t         = {v_t:<4f}")
        print(f"i_n         = {i_n:<4f}")
        print(f"phi_08      = {phi_08:<4f}")
        print(f"phi_10      = {phi_10:<4f}")
        print(f"alpha_ind   = {alpha_ind:<4f}")
        print(f"alpha_cap   = {alpha_cap:<4f}")
        print(f"alpha_uni_c = {alpha_uni_c:<4f}")
        print(f"alpha_uni_i = {alpha_uni_i:<4f}")
        print(f"i_a         = {i_a:<4f}")

        return res

        # print(f"v_t = {}")
        # print(f"v_t = {}")
        # print(f"v_t = {}")
        # print(f"v_t = {}")
        # print(f"v_t = {}")
        # print(f"v_t = {}")
    
     