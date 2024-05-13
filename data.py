import streamlit as st
from streamlit_gsheets import GSheetsConnection

class InvestData:
    def __init__(self, assets, stocks, currencies, trades):
        self.assets = assets
        self.stocks = stocks
        self.currencies = currencies
        self.trades = trades
        
    def hash_func(obj):
        return hash(hash(obj.assets.to_string()) + hash(obj.stocks.to_string()) + hash(obj.currencies.to_string()) + hash(obj.trades.to_string()))
    
    def get_assets(self):
        # Trades consist of a date, asset, amount, price, currency, represented by columns Time, Asset. Amount, Price, Currency, Proceeds
        gains = self.trades.groupby('Asset')['Amount'].sum().to_frame()
        losses = self.trades.groupby('Currency')['Proceeds'].sum().to_frame()
        # Join gains and losses into one DataFrame
        gain_loss = gains.join(losses, how='outer').fillna(0)
        gain_loss['Current'] = gain_loss['Amount'] - gain_loss['Proceeds']
        return gain_loss['Current'].to_frame().rename(columns={'Current': 'Amount'})

    def get_currency_names(self):
        return self.currencies['From'].unique().to_list()
    
    def get_asset_names(self):
        return self.stocks.index.to_list()

def get_investments():
    if 'data' not in st.session_state:
        st.session_state.data = load_investments()
    return st.session_state.data

def load_investments():
    conn = st.connection("gsheets", type=GSheetsConnection)

    assets = conn.read(worksheet='Overview')
    assets = assets.iloc[:, :2].set_index('Asset').dropna()

    stock_prices = conn.read(worksheet='Stocks')
    stock_prices = stock_prices.iloc[:, :3].set_index('Ticker').dropna()
    
    currencies = conn.read(worksheet='Currencies')
    currencies = currencies.iloc[:, :4].set_index('FromTo').dropna()
    
    trades = conn.read(worksheet='Trades')
    trades = trades.iloc[:, :6].dropna()
    
    return InvestData(assets, stock_prices, currencies, trades)

    
