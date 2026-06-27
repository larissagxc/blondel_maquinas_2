import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from dados import Dados

st.set_page_config(layout="wide")

st.title('Diagrama de Blondel de máquinas síncronas de polos salientes')

c1, c2, c3 = st.columns([1, 2, 2])

c1.subheader("Entrada de dados")

dados_modelo = Dados("dados/dados.txt",).dados_brutos
c1.download_button(label="Arquivo modelo", file_name="dados.txt", data=dados_modelo, icon=":material/download:")
arquivo = c1.file_uploader(label='Arquivo de entrada de dados')
if arquivo is not None:
    dados = Dados(StringIO(arquivo.getvalue().decode("utf-8")))
    valido, msg = dados.validar()
    if not valido:
        c1.warning(msg)

i_ex_em_pu_in = c1.toggle(label="Corrente em $pu$?")
i_ex_in = c1.number_input(label=f"Corrente de Excitação [{'PU' if i_ex_em_pu_in else '%'}]")
modo_maquina_in = c1.radio(label="Modo da máquina", options=["Motor", "Gerador"])

fp_in = c1.slider(label="Fator de potência", min_value=0.01, max_value=1.0, step=0.01)

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

c3.subheader('Curva')

x = np.arange(-6, 6, 0.1)
y = 5*fp_in*np.exp(-x**2)

f, ax = plt.subplots()

# 5. Format plot settings
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel(r"Real $\mathbb{R}$")
ax.set_ylabel(r"Imaginário $\mathbb{I}$")
ax.set_title(f"Curva que nao sei o que era pra ser com FP={fp_in}")
ax.grid(True, which="both", linestyle=":", alpha=0.7)
ax.set_aspect("equal")  # Critical so the vectors don't look distorted

ax.plot(x,y)

c3.pyplot(f)