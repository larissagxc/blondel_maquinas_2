import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from dados import Dados
from diagramas import Diagramas
from maquina import Maquina


# Configurações iniciais do layout da página
st.set_page_config(layout="wide")


# Layout para entrada de dados
st.title('Diagrama de Blondel de máquinas síncronas de polos salientes')
c1, c2, c3 = st.columns([1, 2, 2])
c1.subheader("Entrada de dados")

# Cria uma string com o arquivo modelo para auxiliar o usuário na entrada de dados
dados_modelo = Dados("dados/dados.txt",).dados_brutos
c1.download_button(label="Arquivo modelo", file_name="dados.txt", data=dados_modelo, icon=":material/download:")
# Recebe o arquivo do usuário
arquivo = c1.file_uploader(label='Arquivo de entrada de dados', max_upload_size=None)

## Coleta de dados auxiliares
i_ex_em_pu_in   = c1.toggle(label="Corrente em $pu$?")
modo_maquina_in = c1.radio(label="Modo da máquina", options=["Motor", "Gerador"])
i_ex_in         = c1.number_input(label=f"Corrente de Excitação [{'PU' if i_ex_em_pu_in else '%'}]")
tipo_fp_in      = c1.segmented_control(label="Característica do FP", options=["Indutivo", "Capacitivo"], default="Indutivo")
fp_in           = c1.slider(label=f"Fator de potência", min_value=0.0, max_value=1.0, step=0.05, value = 0.8)

## Validação e entrada dos dados
dados_entrada = None
maquina = None
if arquivo is not None:
    dados_entrada = Dados(StringIO(arquivo.getvalue().decode("utf-8")))
    valido, msg = dados_entrada.validar()
    if not valido:
        c1.warning(msg)
    else:
        c1.write("Parâmetros lidos da máquina:")
        c1.write(dados_entrada.dados)
        maquina = Maquina(dados=dados_entrada.dados_limpos, dados_interface={"fp": fp_in, "tipo_fp": tipo_fp_in, "motor_ou_gerador": modo_maquina_in})
        # c1.write(maquina.resultados_maquina())

# Diagrama de Blondel
c2.subheader('Diagrama de blondel')


# Cria um espaço pro gráfico
fig, ax = plt.subplots()

if maquina is not None:
    res = maquina.resultados_maquina()

    v_t     = res["v_t"]
    i_a     = res["i_a"]
    i_d     = res["id_phasor"]
    i_q     = res["iq_phasor"]
    fasor_a = res["fasor_a"]
    E_f     = res["E_f"]
    delta   = res["delta"]

    # Escalona os fasores ao redor de v_t
    v_mag = np.abs(v_t)
    i_a_scaled = i_a * v_mag
    i_d_scaled = i_d * v_mag
    i_q_scaled = i_q * v_mag

    phasors = np.array([v_t, i_a_scaled, i_d_scaled, i_q_scaled, fasor_a, E_f])
    labels  = [r"$V_t$", r"$I_a$", r"$I_d$", r"$I_q$", r"$E_q$", r"$E_f$"]
    colors  = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown"]

    x = np.zeros(len(phasors))
    y = np.zeros(len(phasors))
    u = np.real(phasors)
    v = np.imag(phasors)


    ax.quiver(x, y, u, v, angles="xy", scale_units="xy", scale=1, color=colors)

    for ui, vi, lab in zip(u, v, labels):
        ax.text(ui, vi, lab, fontsize=10, ha='center', va='bottom')

    legend_handles = [Patch(color=c, label=l) for c, l in zip(colors, labels)]
    ax.legend(handles=legend_handles, fontsize=9, loc="upper right")

    max_lim = max(np.max(np.abs(u)), np.max(np.abs(v))) * 1.25
    ax.set_xlim(-max_lim, max_lim)
    ax.set_ylim(-max_lim, max_lim)
    ax.set_xlabel(r"Real $\mathbb{R}$")
    ax.set_ylabel(r"Imaginário $\mathbb{I}$")
    ax.set_title(f"Diagrama de Blondel — {modo_maquina_in}, FP = {fp_in} ({tipo_fp_in})")
    ax.grid(True, which="both", linestyle=":", alpha=0.7)
    ax.set_aspect("equal")

    c2.write(f"FP = {fp_in} ({tipo_fp_in}), Modo: {modo_maquina_in}, "
             rf"$\delta$ = {np.degrees(delta):.2f}°, "
             rf"$\phi$ = {np.degrees(res['phi']):.2f}°")
else:
    c2.write("Carregue um arquivo de dados para visualizar o diagrama.")

c2.pyplot(fig)


# Curva de carga
c3.subheader('Curva')

x = np.arange(-6, 6, 0.1)
y = 5*fp_in*np.exp(-x**2) if tipo_fp_in == "Indutivo" else -5*fp_in*np.exp(-x**2)

f, ax = plt.subplots()

# 5. Format plot settings
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel(r"Real $\mathbb{R}$")
ax.set_ylabel(r"Imaginário $\mathbb{I}$")
ax.set_title(f"Curva que nao sei o que era pra ser com FP={fp_in:.1f}")
ax.grid(True, which="both", linestyle=":", alpha=0.7)
ax.set_aspect("equal")  # Critical so the vectors don't look distorted

ax.plot(x,y)

c3.pyplot(f)

