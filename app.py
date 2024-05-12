import streamlit as st
import gspread
from streamlit_gsheets import GSheetsConnection

st.title('Investment Simulator')

# gc = gspread.service_account()
# ss = gc.list_spreadsheet_files()
# sh = gc.open('Honzík investice')

# st.caption(sh.sheet1.get('A1'))

conn = st.connection("gsheets", type=GSheetsConnection)
assets = conn.read(worksheet='Overview')
stocks = conn.read(worksheet='Stocks')
currency = conn.read(worksheet='Currencies')

# Keep only the first three columns
assets = assets.iloc[:, :2]
stocks = stocks.iloc[:, :3]
currency = currency.iloc[:, :3]

st.dataframe(assets)
st.dataframe(stocks)
st.dataframe(currency)