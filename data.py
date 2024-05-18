import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

class StoredData:
    def __init__(self, trades, stocks, currencies):
        self.trades = trades
        self.stocks = stocks
        self.currencies = currencies
        
    @staticmethod
    def load_from_sheets(progress, text):
        conn = st.connection("gsheets", type=GSheetsConnection)
        progress.progress(0.2, text=text)

        sheet = conn.read(worksheet='Honzik')

        trades = sheet.iloc[:, :6].dropna()
        trades['Time'] = pd.to_datetime(trades['Time'], dayfirst=True)
        progress.progress(0.3, text=text)

        stock_prices = sheet.iloc[:, 7:10].set_index('Ticker').dropna().rename(columns={'T.Price': 'Price', 'T.Currency': 'Currency'})
        progress.progress(0.6, text=text)

        currencies = sheet.iloc[:, 11:15].set_index('FromTo').dropna().rename(columns={'C.Price': 'Price'})

        sheet = pd.concat([trades.reset_index(), pd.DataFrame(columns=['S.Spacer']), stock_prices.reset_index(), pd.DataFrame(columns=['C.Spacer']), currencies.reset_index()], axis=1)
        conn.update(data=sheet, worksheet='Honzik')
        
        progress.progress(1.0, text='Hotovo')
        progress.empty()
        
        return StoredData(trades, stock_prices, currencies)
    
    def save_to_sheets(self):
        # Merge all data into one DataFrame
        sheet = pd.concat([self.trades.reset_index(), pd.DataFrame(columns=['S.Spacer']), self.stocks.reset_index(), pd.DataFrame(columns=['C.Spacer']), self.currencies.reset_index()], axis=1)
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.update(data=sheet, worksheet='Honzik')
    
    def update_trades(self, trades):
        self.save_to_sheets()


class Investments:
    def __init__(self, stored_data : StoredData):
        self.stored_data = stored_data
        self.assets = None
        self.stocks = stored_data.stocks.copy()
        self.currencies = stored_data.currencies.copy()
        self._trades = stored_data.trades.copy()
        
    def hash_func(obj):
        return hash( hash(obj.stocks.to_string()) + hash(obj.currencies.to_string()) + hash(obj._trades.to_string()))
    
    def get_trades(self):
        return self._trades
    
    def get_assets(self):
        if self.assets is not None:
            return self.assets
        # Trades consist of a date, asset, amount, price, currency, represented by columns Time, Asset. Amount, Price, Currency, Proceeds
        gains = self._trades.groupby('Asset')['Amount'].sum().to_frame()
        losses = self._trades.groupby('Currency')['Proceeds'].sum().to_frame()
        # Join gains and losses into one DataFrame
        gain_loss = gains.join(losses, how='outer').fillna(0)
        gain_loss['Current'] = gain_loss['Amount'] - gain_loss['Proceeds']
        return gain_loss[gain_loss['Current'] != 0]['Current'].to_frame().rename(columns={'Current': 'Amount'})

    def get_currency_names(self):
        return self.currencies['From'].unique().to_list()
    
    def get_asset_names(self):
        return self.stocks.index.to_list()
    
    def buy(self, asset, amount, currency):
        self._trades = self._trades.append({'Time': pd.Timestamp.now(), 'Asset': asset, 'Amount': amount, 'Currency': currency, 'Price': self.stocks.loc[asset, 'Price'], 'Proceeds': amount * self.stocks.loc[asset, 'Price']}, ignore_index=True)
        self.assets = None
    
    def sell(self, asset, amount, currency):
        self.buy(asset, -amount, currency)
    
    def save(self):
        self.stored_data.update_trades(self._trades)

def get_investments():
    if 'data' not in st.session_state:
        st.session_state.data = load_investments()
    return st.session_state.data

def load_investments():
    text = 'Načítám data o investicích...'
    progress = st.progress(0, text=text)
    persister = StoredData.load_from_sheets(progress, text)    
    return Investments(persister)


