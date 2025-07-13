import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from modules.data_provider import FinanceDataService
from datetime import datetime, timedelta

class FinanceUI:
    def __init__(self):
        self.data_service = FinanceDataService()
        self.graph_types = {
            'Linha': self._plot_line,
            'Candlestick': self._plot_candlestick,
            'Barras': self._plot_bar
            #'Área': self._plot_area
        }
    
    def run(self) -> None:
        """Executa a aplicação principal"""
        st.set_page_config(layout="wide")
        st.title("📈 Análise Financeira")
        
        tickers, start_date, end_date, analysis_type = self._build_sidebar()
        
        if st.sidebar.button("Executar Análise", type="primary"):
            self._display_results(tickers, start_date, end_date, analysis_type)
    
    def _build_sidebar(self):
        """Constroi a barra lateral"""
        with st.sidebar:
            st.header("⚙️ Configurações")
            
            # Input de tickers
            ticker_input = st.text_input(
                "Ativos (separar por vírgula, quando comparar ativos):",
                "PETR4.SA, VALE3.SA",
                help="Ex: PETR4.SA, VALE3.SA, ITUB4.SA"
            )
            tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
            
            # Controles de data
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Data inicial:",
                    datetime.now() - timedelta(days=365),
                    max_value=datetime.now() - timedelta(days=1)
                )
            with col2:
                end_date = st.date_input(
                    "Data final:",
                    datetime.now(),
                    min_value=start_date + timedelta(days=1))
            
            # Tipo de análise
            analysis_type = st.radio(
                "Tipo de análise:",
                ['Histórico', 'Comparação', 'Previsão'],
                index=0
            )
            
            # Tipo de gráfico (apenas para histórico/comparação)
            if analysis_type in ['Histórico', 'Comparação']:
                graph_type = st.selectbox(
                    "Tipo de gráfico:",
                    list(self.graph_types.keys()),
                    index=0  # Default -> Linha
                )
            else:
                graph_type = 'Linha'  # Setar linha para Previsão
            
            return tickers, start_date, end_date, (analysis_type, graph_type)
    
    def _display_results(self, tickers: str, start_date, end_date, analysis_config) -> None:
        """Exibe os resultados conforme configuração"""
        analysis_type, graph_type = analysis_config
        
        with st.spinner("Obtendo dados..."):
            if analysis_type == 'Comparação' and len(tickers) < 2:
                st.error("Selecione pelo menos 2 ativos para comparação")
                return
            
            data_dict = self.data_service.get_multiple_data(tickers, start_date, end_date)
            
            if not data_dict:
                st.error("Nenhum dado encontrado para os ativos selecionados")
                return
            
            st.header(f"📊 Resultados - {analysis_type}")
            
            if analysis_type == 'Histórico':
                for ticker, data in data_dict.items():
                    self._show_single_asset(ticker, data, graph_type)
            elif analysis_type == 'Comparação':
                self._show_comparison(data_dict, graph_type)
            else:  # Previsão
                for ticker, data in data_dict.items():
                    self._show_forecast(ticker, data)
    
    def _show_single_asset(self, ticker, data, graph_type):
        """Mostra análise individual"""
        st.subheader(ticker)
        self.graph_types[graph_type](data, ticker)
        st.dataframe(data.tail(10), use_container_width=True)
    
    def _show_comparison(self, data_dict, graph_type):
        """Mostra comparação entre ativos"""
        # Normaliza os dados para comparação relativa
        # normalized = {}
        # for ticker, data in data_dict.items():
        #     first_close = data['Fechamento'].iloc[0]
        #     normalized[ticker] = data.assign(
        #         Normalized=(data['Fechamento'] / first_close) * 100
        #     )
        
        # Gráfico comparativo
        fig = go.Figure()
        
        for ticker, data in data_dict.items():
            if graph_type == 'Candlestick':
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Abertura'],
                    high=data['Alta'],
                    low=data['Baixa'],
                    close=data['Fechamento'],
                    name=ticker
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    # y=data['Normalized' if graph_type != 'Candlestick' else 'Fechamento'],
                    y=data['Fechamento'],
                    name=ticker,
                    mode='lines' if graph_type == 'Linha' else None,
                    marker=dict(color='blue') if graph_type == 'Barras' else None
                ))
        
        # title_suffix = "Normalizado (Base 100)" if graph_type != 'Candlestick' else "Preços Absolutos"
        title_suffix = "Preços Absolutos"
        fig.update_layout(
            title=f"Comparação {title_suffix}",
            height=500,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_forecast(self, ticker, data):
        """Mostra previsão usando Regressão Linear"""
        
        try:
            # Prepara os dados para regressão linear
            X = np.arange(len(data)).reshape(-1, 1)  # Dias como variável independente
            y = data['Fechamento'].values  # Preços como variável dependente
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Faz a previsão para os próximos 7 dias
            future_days = np.arange(len(data), len(data) + 7).reshape(-1, 1)
            forecast = model.predict(future_days)
            
            # Criando a figura
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Fechamento'],
                name="Histórico",
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=pd.date_range(data.index[-1], periods=7)[1:],
                y=forecast,
                name="Previsão Linear",
                line=dict(color='red', dash='dot')
            ))
            
            # Adiciona linha de tendência
            trend_line = model.predict(X)
            fig.add_trace(go.Scatter(
                x=data.index,
                y=trend_line,
                name="Tendência",
                line=dict(color='green', width=2, dash='dash')
            ))
            
            # Configurações do layout
            fig.update_layout(
                title=f"Previsão Linear para {ticker}",
                height=500,
                hovermode="x unified",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # r_squared = model.score(X, y)
            # st.caption(f"R² do modelo: {r_squared:.4f} | Inclinação: {model.coef_[0]:.4f}")
            
        except Exception as e:
            st.error(f"Erro na previsão linear: {str(e)}")
    
    # Métodos de plotagem
    def _plot_line(self, data, ticker):
        fig = px.line(data, x=data.index, y='Fechamento', title=f"{ticker} - Série Temporal")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_candlestick(self, data, ticker):
        fig = go.Figure(data=[
            go.Candlestick(
                x=data.index,
                open=data['Abertura'],
                high=data['Alta'],
                low=data['Baixa'],
                close=data['Fechamento']
            )
        ])
        fig.update_layout(
            title=f"{ticker} - Candlestick",
            xaxis_rangeslider_visible=True,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_bar(self, data, ticker):
        fig = px.bar(data, x=data.index, y='Volume', title=f"{ticker} - Volume")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    def _plot_area(self, data, ticker):
        fig = px.area(data, x=data.index, y='Fechamento', title=f"{ticker} - Variação")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)