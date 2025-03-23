# Análise de Risco e Retorno de Carteiras de Investimentos usando Simulações de Monte Carlo e Otimização com Python

Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) da Pós-graduação em Matemática Financeira e Estatística do **Instituto Educaminas EAD**. O objetivo é criar uma aplicação interativa que permita a análise de risco e retorno de carteiras de investimentos utilizando técnicas de Simulação de Monte Carlo e otimização de carteiras.

A aplicação foi desenvolvida em **Python** e utiliza a biblioteca **Streamlit** para criar uma interface web interativa. O código está disponível no GitHub e pode ser facilmente executado localmente ou publicado online.

## **Funcionalidades**

1. **Seleção de Ativos**: O usuário pode selecionar os ativos que deseja incluir na carteira.
2. **Período de Análise**: É possível definir o período de análise dos dados históricos.
3. **Otimização de Carteira**: O programa calcula os pesos otimizados para maximizar o retorno e minimizar o risco, utilizando a Teoria Moderna de Carteiras (Markowitz).
4. **Simulação de Monte Carlo**: Realiza simulações para prever cenários futuros de retorno e risco.
5. **Visualização Gráfica**: Apresenta gráficos interativos para análise dos resultados.

## **Como Executar o Projeto**

### **Pré-requisitos**

- Python 3.8 ou superior instalado.
- Bibliotecas listadas no arquivo `requirements.txt`.

### **Passos para Execução**

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio

2. Atualize o `requirements.txt`:
O `numpy==2.0.0` pode não ser a melhor escolha para o seu ambiente. Vamos usar uma versão mais estável e amplamente compatível. Atualize o `requirements.txt` para:
   ```plaintext
    streamlit==1.43.2
    numpy==1.26.0
    pandas==2.2.3
    yfinance==0.2.18
    matplotlib==3.8.0
    plotly==5.18.0
    scipy==1.12.0