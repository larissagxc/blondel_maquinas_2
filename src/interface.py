import matplotlib.pyplot as plt
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
arquivo = c1.file_uploader(label='Arquivo de entrada de dados')

## Coleta de dados auxiliares
i_ex_em_pu_in   = c1.toggle(label="Corrente em $pu$?")
modo_maquina_in = c1.radio(label="Modo da máquina", options=["Motor", "Gerador"])
i_ex_in         = c1.number_input(label=f"Corrente de Excitação [{'PU' if i_ex_em_pu_in else '%'}]")
tipo_fp_in      = c1.segmented_control(label="Característica do FP", options=["Indutivo", "Capacitivo"])
fp_in           = c1.slider(label=f"Fator de potência", min_value=0.0, max_value=1.0, step=0.05, value = 0.8)

## Validação e entrada dos dados


dados_entrada = None
if arquivo is not None:
    dados_entrada = Dados(StringIO(arquivo.getvalue().decode("utf-8")))
    valido, msg = dados_entrada.validar()
    if not valido:
        c1.warning(msg)
    else:
        c1.write("Parâmetros lidos da máquina:")
        c1.write(dados_entrada.dados)
        maq = Maquina(dados=dados_entrada.dados_limpos, dados_interface={"fp": fp_in, "tipo_fp": tipo_fp_in})
        c1.write(maq.resultados_maquina())






# Diagrama de Blondel
c2.subheader('Diagrama de blondel')

phasors = np.array([3 + 4j, 5 - 2j, 2 -4j, -2-4j])

# 2. Extract real (X, U) and imaginary (Y, V) parts
x = np.zeros(len(phasors))
y = np.zeros(len(phasors))
u = np.real(phasors)
v = np.imag(phasors)

# 3. Create the quiver plot
fig, ax = plt.subplots(figsize=(6, 6))

# Plot the vectors with specific formatting for data coordinates
# We set color and label for clarity
q = ax.quiver(
    x,
    y,
    u,
    v,
    angles="xy",
    scale_units="xy",
    scale=1,
    color=["tab:blue", "tab:orange", "tab:green"],
    
)

# 5. Format plot settings
ax.axhline(0, color="gray", linewidth=1.5)
ax.axvline(0, color="gray", linewidth=1.5)
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel(r"Real $\mathbb{R}$")
ax.set_ylabel(r"Imaginário $\mathbb{I}$")
ax.set_title("Phasor Diagram using Matplotlib Quiver")
ax.grid(True, which="both", linestyle=":", alpha=0.7)
ax.set_aspect("equal")  # Critical so the vectors don't look distorted


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

# st.divider()

# st.header("Dados processados:")

# # tab_dados = pd.DataFrame(data=)

