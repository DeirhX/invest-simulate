import streamlit as st
from menu import menu
from data import get_investments

st.set_page_config(page_title='Ceny akcií', layout='centered')
st.subheader('Aktuální ceny akcií')
menu()

data = get_investments()
st.dataframe(data.stocks, hide_index=False, 
             column_order=['Ticker', 'Currency', 'Price'], 
             column_config={'Ticker': st.column_config.TextColumn("Kód"),
                            'Price': st.column_config.NumberColumn("Cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna")})