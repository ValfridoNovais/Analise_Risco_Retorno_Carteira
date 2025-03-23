import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Função para calcular retorno e risco da carteira
def calcular_retorno_risco(pesos, retornos, cov_matrix):
    retorno = np.dot(pesos, retornos)
    risco = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))
    return retorno, risco

# Função para otimizar a carteira
def otimizar_carteira(retornos, cov_matrix):
    num_ativos = len(retornos)
    args = (retornos, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_ativos))
    resultado = minimize(lambda x: -calcular_retorno_risco(x, retornos, cov_matrix)[0], num_assets * [1. / num_ativos], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return resultado.x

# Interface do Streamlit
st.title("Otimização de Carteira de Investimentos")

# Seleção de ativos
ativos = st.multiselect("Selecione os ativos", ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"], default=["AAPL", "GOOG", "MSFT"])

# Período de análise
inicio = st.date_input("Data de início", pd.to_datetime("2020-01-01"))
fim = st.date_input("Data de fim", pd.to_datetime("2023-01-01"))

# Baixar dados
dados = yf.download(ativos, start=inicio, end=fim)['Adj Close']
retornos = dados.pct_change().dropna()
cov_matrix = retornos.cov()
retornos_medios = retornos.mean()

# Otimização
pesos_otimizados = otimizar_carteira(retornos_medios, cov_matrix)
retorno_otimizado, risco_otimizado = calcular_retorno_risco(pesos_otimizados, retornos_medios, cov_matrix)

# Resultados
st.write("### Pesos Otimizados")
for ativo, peso in zip(ativos, pesos_otimizados):
    st.write(f"{ativo}: {peso:.2%}")

st.write(f"Retorno Esperado: {retorno_otimizado:.2%}")
st.write(f"Risco (Volatilidade): {risco_otimizado:.2%}")

# Gráfico
fig, ax = plt.subplots()
ax.pie(pesos_otimizados, labels=ativos, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)s