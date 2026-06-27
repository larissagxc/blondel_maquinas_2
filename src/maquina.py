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
        """
        Calcula a corrente Ia a partir do cálculo de alpha
        """
        alpha = self.calc_alpha()
        i_a = np.cos(alpha) + 1j*np.sin(alpha)
        return i_a
    
    def calc_fasor_aux(self) -> complex:
        """
        Calcula o fasor auxuliar com v_t e i_a.
        Consome da interface se a máquina opera como motor ou gerador
        """
        v_t = self.calc_v_t()
        i_a = self.calc_ia()
        # modo = 1 -> Motor, modo = -1 -> gerador
        modo = 1 if self.dados_interface["motor_ou_gerador"] == "Gerador" else -1
        fasor_a = v_t + modo*(self.dados['Ra']*i_a + 1j*self.dados["Xq"]*i_a)
        return fasor_a
    
    def calc_delta(self) -> complex:
        """
        Calcula o valor de delta a partir do fasor auxiliar
        """
        fasor_a = self.calc_fasor_aux()
        return np.angle(fasor_a)

    
    def calc_id(self) -> complex:
        """
        Calcula corrente i_d a partir de i_a, delta e
        """
        i_a = self.calc_ia()
        delta = self.calc_delta()
        alpha = self.calc_alpha()
        i_d = i_a * np.sin(delta - alpha)
        return i_d

    def calc_iq(self) -> complex:
        """
        Calcula corrente iq a partir de i_a, delta e
        """
        i_a = self.calc_ia()
        delta = self.calc_delta()
        alpha = self.calc_alpha()
        i_q = i_a * np.cos(delta - alpha)
        return i_q
        
    def calc_ef(self) -> complex:
        """
        Calcula o valor de E_F decompondo parcialmente os resultados
        """
        i_d      =  self.calc_id()
        delta    =  self.calc_delta()
        xd_xq_id = (self.dados['Xd'] - self.dados['Xq']) * i_d
        fasor_a  =  self.calc_fasor_aux()
        # modo = 1 -> Motor, modo = -1 -> gerador
        modo = 1 if self.dados_interface["motor_ou_gerador"] == "Gerador" else -1
        
        ef_abs = np.abs(fasor_a) + modo*xd_xq_id
        ef = ef_abs*np.cos(delta) + 1j*ef_abs*np.sin(delta)
        return ef


    def resultados_maquina(self) -> Dict[str, np.number]:
        """
        Função auxiliar que realiza todos os cálculos e retorna um dicionário com o nome da variável e o valor correspondente
        """

        res = {
            "v_t":            self.calc_v_t(),
            "i_n":            self.calc_i_n(),
            "phi":            self.calc_phi(),
            "alpha":          self.calc_alpha(),
            "i_a":            self.calc_ia(),
            "i_q":            self.calc_iq(),
            "i_d":            self.calc_id(),
            "fasor_a":        self.calc_fasor_aux(),
            "delta":          self.calc_delta(),
            "E_f":            self.calc_ef(),
            "id_phasor":      None,
            "iq_phasor":      None,
        }

        v_t           = self.calc_v_t()
        i_n           = self.calc_i_n()
        phi           = self.calc_phi()
        alpha         = self.calc_alpha()
        i_a           = self.calc_ia()
        fasor_a       = self.calc_fasor_aux()
        delta         = self.calc_delta()
        E_f           = self.calc_ef()

        # Proper phasors oriented along d-axis (δ - π/2) and q-axis (δ)
        i_d_mag = np.abs(i_a) * np.sin(delta - alpha)
        i_q_mag = np.abs(i_a) * np.cos(delta - alpha)
        id_phasor = i_d_mag * np.exp(1j * (delta - np.pi/2))
        iq_phasor = i_q_mag * np.exp(1j * delta)
        res["id_phasor"] = id_phasor
        res["iq_phasor"] = iq_phasor

        print(f"v_t         = {v_t:<4f}")
        print(f"i_n         = {i_n:<4f}")
        print(f"phi         = {phi:<4f}")
        print(f"alpha       = {alpha:<4f}")
        print(f"i_a         = {i_a:<4f}")
        print(f"fasor_a     = {fasor_a:<4f}")
        print(f"delta       = {delta:<4f}")
        print(f"E_f         = {E_f:<4f}")
        print(f"id_phasor   = {id_phasor:<4f}")
        print(f"iq_phasor   = {iq_phasor:<4f}")

        return res

    
     