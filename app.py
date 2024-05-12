import streamlit as st
import gspread
from streamlit_gsheets import GSheetsConnection
from menu import menu
from data import get_investments
import compute

st.title('Investiční simulátor')

# gc = gspread.service_account()
# ss = gc.list_spreadsheet_files()
# sh = gc.open('Honzík investice')

# st.caption(sh.sheet1.get('A1'))

menu()
data = get_investments()

st.markdown('Aktuální majetek')
st.dataframe(compute.assets_with_prices(data), hide_index=True,
             column_order=['Asset', 'Amount', 'Price', 'Currency', 'Value'], 
             column_config={'Asset': st.column_config.TextColumn("Instrument"),
                            'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                            'Price': st.column_config.NumberColumn("Cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna"),
                            'Value': st.column_config.NumberColumn("Hodnota", format="%.2f")})
col1, col2 = st.columns([1, 2])
with col1:
    base_currency = st.selectbox('Přepočet na', ['USD', 'CZK', 'EUR'], key='base_currency')
st.markdown(f'Aktuální hodnota: {compute.wealth_in_currency(data, base_currency):.2f} {base_currency}')