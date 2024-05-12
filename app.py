import streamlit as st
import gspread
from streamlit_gsheets import GSheetsConnection
from menu import menu
from data import get_investments
from compute import wealth_in_currency

st.title('Investiční simulátor')

# gc = gspread.service_account()
# ss = gc.list_spreadsheet_files()
# sh = gc.open('Honzík investice')

# st.caption(sh.sheet1.get('A1'))

menu()

data = get_investments()

st.markdown('Aktuální majetek')
st.dataframe(data.assets, hide_index=True,
             column_order=['Asset', 'Amount'], 
             column_config={'Asset': st.column_config.TextColumn("Instrument"),
                            'Amount': st.column_config.NumberColumn("Množství", format="%.2f")})
col1, col2 = st.columns([1, 2])
with col1:
    base_currency = st.selectbox('Přepočet na', data.assets.index, key='base_currency')
st.markdown(f'Aktuální hodnota: {wealth_in_currency(data, base_currency):.2f} {base_currency}')

st.dataframe(data.stocks)
st.dataframe(data.currencies)