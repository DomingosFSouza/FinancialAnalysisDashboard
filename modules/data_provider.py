import os
import pandas as pd
import yfinance as yf
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

class DataProvider(ABC):
    """Interface para provedores de dados"""
    @abstractmethod
    def get_historical_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass

class YahooFinanceProvider(DataProvider):
    """Implementação para Yahoo Finance com tratamento de fallback"""
    def get_historical_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=True
            )
            
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['Abertura', 'Alta', 'Baixa', 'Fechamento', 'Volume']

            return data if not data.empty else None
        except Exception as e:
            print(f"Erro no Yahoo Finance ({ticker}): {str(e)}")
            return None

class AlphaVantageProvider(DataProvider):
    """Implementação para Alpha Vantage como fallback"""
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_KEY') or "DEFAULT"
        
    def get_historical_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.api_key}&outputsize=full"
            response = requests.get(url).json()
            
            # Transforma os dados no mesmo formato do Yahoo Finance
            data = pd.DataFrame(
                response['Time Series (Daily)']
            ).T.apply(pd.to_numeric)
            
            data.index = pd.to_datetime(data.index)
            data.columns = ['Abertura', 'Alta', 'Baixa', 'Fechamento', 'Volume']
            
            # Filtra pelo período solicitado
            mask = (data.index >= pd.to_datetime(start_date)) & (data.index <= pd.to_datetime(end_date))
            return data.loc[mask].sort_index()
            
        except Exception:
            return None

class FinanceDataService:
    """Serviço unificado com fallback automático"""
    def __init__(self):
        self.providers = [
            YahooFinanceProvider(), 
            AlphaVantageProvider()
        ]
    
    def get_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Tenta cada provedor até obter dados válidos"""
        for provider in self.providers:
            data = provider.get_historical_data(ticker, start_date, end_date)
            if data is not None and not data.empty:
                return data
        return None
    
    def get_multiple_data(self, tickers: List[str], start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """Obtém dados para múltiplos tickers"""
        results = {}
        for ticker in tickers:
            data = self.get_data(ticker, start_date, end_date)
            if data is not None:
                results[ticker] = data
        return results