import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime, timedelta

# Função para baixar dados do yfinance
def baixar_dados(ativo, inicio, fim):
    try:
        dados = yf.download(ativo, start=inicio, end=fim)['Adj Close']
        return dados
    except Exception as e:
        st.error(f"Erro ao baixar dados para {ativo}: {e}")
        return pd.Series()  # Retorna uma série vazia em caso de erro

# Função para calcular retorno e risco da carteira
def calcular_retorno_risco(pesos, retornos, cov_matrix):
    retorno = np.dot(pesos, retornos)
    risco = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))
    return retorno, risco

# Função para otimizar a carteira
def otimizar_carteira(retornos, cov_matrix):
    num_ativos = len(retornos)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_ativos))
    
    # Função objetivo ajustada para receber os argumentos corretamente
    def funcao_objetivo(x, retornos, cov_matrix):
        return -calcular_retorno_risco(x, retornos, cov_matrix)[0]
    
    resultado = minimize(
        funcao_objetivo,  # Usando a função objetivo corrigida
        num_ativos * [1. / num_ativos],  # Chute inicial
        args=(retornos, cov_matrix),  # Argumentos adicionais
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    return resultado.x

# Interface do Streamlit
st.title("Otimização de Carteira de Investimentos")

# Seleção do mercado
mercado = st.selectbox("Selecione o mercado", ["Principais Bolsas (NYSE/NASDAQ)", "B3 (Bolsa Brasileira)"])

# Seleção de ativos
if mercado == "Principais Bolsas (NYSE/NASDAQ)":
    ativos_padrao = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]
else:
    ativos_padrao = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA"]  # Exemplos de ações da B3

ativos = st.multiselect("Selecione os ativos", ativos_padrao, default=ativos_padrao[:3])

# Período de análise
inicio = st.date_input("Data de início", pd.to_datetime("2020-01-01"))
fim = st.date_input("Data de fim", datetime.now().date())  # Data de fim editável, inicializada com o dia atual

# Botão para confirmar e baixar dados
if st.button("Confirmar e Baixar Dados"):
    if not ativos:
        st.error("Por favor, selecione pelo menos um ativo.")
    else:
        # Baixar dados
        dados = pd.DataFrame()
        for ativo in ativos:
            dados_ativo = baixar_dados(ativo, inicio, fim)
            if not dados_ativo.empty:
                dados[ativo] = dados_ativo

        if dados.empty:
            st.error("Nenhum dado foi encontrado para os ativos selecionados no período especificado.")
        else:
            # Verificar se há dados para cada ativo
            ativos_validos = [ativo for ativo in ativos if ativo in dados.columns]
            if not ativos_validos:
                st.error("Nenhum ativo válido foi encontrado.")
            else:
                # Calcular retornos e covariância
                retornos = dados[ativos_validos].pct_change().dropna()
                cov_matrix = retornos.cov()
                retornos_medios = retornos.mean()

                # Otimização
                pesos_otimizados = otimizar_carteira(retornos_medios, cov_matrix)
                retorno_otimizado, risco_otimizado = calcular_retorno_risco(pesos_otimizados, retornos_medios, cov_matrix)

                # Exibir valor atual de cada ação
                st.write("### Valor Atual dos Ativos")
                for ativo in ativos_validos:
                    valor_atual = dados[ativo].iloc[-1]  # Último valor disponível
                    st.write(f"{ativo}: ${valor_atual:.2f}")

                # Resultados da carteira
                st.write("### Pesos Otimizados")
                for ativo, peso in zip(ativos_validos, pesos_otimizados):
                    st.write(f"{ativo}: {peso:.2%}")

                st.write(f"Retorno Esperado: {retorno_otimizado:.2%}")
                st.write(f"Risco (Volatilidade): {risco_otimizado:.2%}")

                # Gráfico de pizza da carteira
                st.write("### Distribuição da Carteira")
                fig, ax = plt.subplots()
                ax.pie(pesos_otimizados, labels=ativos_validos, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

                # Gráfico de evolução do ativo
                st.write("### Evolução do Ativo")

                # Seleção do ativo para o gráfico
                ativo_grafico = st.selectbox("Selecione um ativo para visualizar a evolução", ativos_validos)

                # Seleção do intervalo do gráfico
                intervalo = st.selectbox("Selecione o intervalo do gráfico", ["Diário", "Semanal", "Mensal", "Anual"])

                # Plotar o gráfico de evolução
                st.write(f"### Evolução do Preço de {ativo_grafico} ({intervalo})")
                fig2, ax2 = plt.subplots()
                ax2.plot(dados[ativo_grafico], label=ativo_grafico)
                ax2.set_xlabel("Data")
                ax2.set_ylabel("Preço (USD)")
                ax2.legend()
                st.pyplot(fig2)