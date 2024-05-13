import streamlit as st
from menu import menu
from data import get_investments
from ux import show_assets_dataframe
import compute

st.title('Investiční simulátor')

menu()

data = st.session_state.get('data', None) or get_investments()
st.session_state.data = data

st.markdown('Aktuální majetek')
show_assets_dataframe(compute.assets_with_prices(data))
col1, col2 = st.columns([1, 2])
with col1:
    base_currency = st.selectbox('Přepočet na', ['USD', 'CZK', 'EUR'], key='base_currency')
st.markdown(f'Aktuální hodnota: {compute.wealth_in_currency(data, base_currency):.2f} {base_currency}')