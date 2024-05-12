import streamlit as st
from streamlit_gsheets import GSheetsConnection

class InvestData:
    def __init__(self, assets, stocks, currencies):
        self.assets = assets
        self.stocks = stocks
        self.currencies = currencies
        
def get_investments():
    conn = st.connection("gsheets", type=GSheetsConnection)

    assets = conn.read(worksheet='Overview')
    assets = assets.iloc[:, :2].set_index('Asset').dropna()

    stock_prices = conn.read(worksheet='Stocks')
    stock_prices = stock_prices.iloc[:, :3].set_index('Ticker').dropna()
    
    currencies = conn.read(worksheet='Currencies')
    currencies = currencies.iloc[:, :4].set_index('FromTo').dropna()
    
    return InvestData(assets, stock_prices, currencies)

    
