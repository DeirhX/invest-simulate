import streamlit as st
import auth
from menu import menu
from data import get_investments

st.set_page_config(page_title='Ceny akcií', layout='centered')
st.subheader('Aktuální ceny akcií')
menu()
auth.need_login()

data = st.session_state.get('data', None) or get_investments()
st.session_state.data = data

st.dataframe(data.stocks, hide_index=False, 
             column_order=['Ticker', 'Currency', 'Price'], 
             column_config={'Ticker': st.column_config.TextColumn("Kód"),
                            'Price': st.column_config.NumberColumn("Cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna")})