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

        stock_prices = conn.read(worksheet='Stocks')
        stock_prices = stock_prices.iloc[:, :3].set_index('Ticker').dropna()
        progress.progress(0.6, text=text)
        
        currencies = conn.read(worksheet='Currencies')
        currencies = currencies.iloc[:, :4].set_index('FromTo').dropna()
        progress.progress(0.8, text=text)
        
        trades = conn.read(worksheet='Trades')
        trades = trades.iloc[:, :6].dropna()
        trades['Time'] = pd.to_datetime(trades['Time'], dayfirst=True)
        progress.progress(1.0, text='Hotovo')
        progress.empty()
      
        return StoredData(trades, stock_prices, currencies)
    
    @staticmethod
    def load_trades():
        conn = st.connection("gsheets", type=GSheetsConnection)
        trades = conn.read(worksheet='Trades')
        trades = trades.iloc[:, :6].dropna()
        trades['Time'] = pd.to_datetime(trades['Time'], dayfirst=True)
        return trades
    
    def add_trade(self, trade):
        conn = st.connection("gsheets", type=GSheetsConnection)
        st.cache_data.clear()
        prev_trades = StoredData.load_trades()
        # Merge trades with current trades, keeping all unique rows
        trades = pd.concat([prev_trades, trade])
        conn.update(data=trades, worksheet='Trades')
        return trades


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
        self.assets = gain_loss[gain_loss['Current'] != 0]['Current'].to_frame().rename(columns={'Current': 'Amount'})
        
        # Now find average purchase price for each asset
        purchases = self._trades[self._trades['Amount'] > 0]
        # For each asset, walk from newest to oldest trades and select enough of them to cover the currently owned amount
        # If the last purchase exceeds the amount, treat it as a partial purchase
        # Next, do a weighted average of the prices
        for asset in self.assets.index:
            asset_trades = purchases[purchases['Asset'] == asset].sort_values(by='Time', ascending=False)
            amount = self.assets.loc[asset, 'Amount']
            price = 0
            for i, row in asset_trades.iterrows():
                if amount <= 0:
                    break
                if row['Amount'] >= amount:
                    price += amount * row['Price']
                    break
                price += row['Amount'] * row['Price']
                amount -= row['Amount']
            self.assets.loc[asset, 'Average Price'] = price / self.assets.loc[asset, 'Amount']
        self.assets['% Profit'] = (self.stocks['Price'] - self.assets['Average Price']) / self.assets['Average Price'] * 100
        return self.assets

    def get_currency_names(self):
        return self.currencies['From'].unique()
    
    def get_exchangable_currencies(self, currency):
        return self.currencies[self.currencies['From'] == currency]['To'].to_list()
    
    def get_exchange_rate(self, source, target):
        return self.currencies[(self.currencies['From'] == source) & (self.currencies['To'] == target)]['Price'].values[0]
    
    def get_asset_names(self):
        return self.stocks.index.to_list()
    
    def buy(self, asset, amount, currency):
        new_trade = pd.DataFrame({'Time': pd.Timestamp.now(),
                      'Asset': asset,
                      'Amount': amount,
                      'Currency': currency,
                      'Price': self.stocks.loc[asset, 'Price'],
                      'Proceeds': amount * self.stocks.loc[asset, 'Price']}, index=[0])
        self._trades = self.stored_data.add_trade(new_trade)
        self.assets = None
    
    def sell(self, asset, amount, currency):
        self.buy(asset, -amount, currency)
    
    def save(self):
        pass

def get_investments():
    if 'data' not in st.session_state:
        st.session_state.data = load_investments()
    return st.session_state.data

def load_investments():
    text = 'Načítám data o investicích...'
    progress = st.progress(0, text=text)
    persister = StoredData.load_from_sheets(progress, text)    
    return Investments(persister)


