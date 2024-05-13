import streamlit as st
from menu import menu
from data import get_investments
import compute

st.title('Investiční simulátor')

menu()
data = get_investments()

st.markdown('Aktuální majetek')
st.dataframe(compute.assets_with_prices(data), hide_index=False,
             column_order=['Asset', 'Amount', 'Price', 'Currency', 'Value'], 
             column_config={'Asset': st.column_config.TextColumn("Instrument"),
                            'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                            'Price': st.column_config.NumberColumn("Aktuální cena", format="%.2f"),
                            'Currency': st.column_config.TextColumn("Měna"),
                            'Value': st.column_config.NumberColumn("Hodnota", format="%.2f")})
col1, col2 = st.columns([1, 2])
with col1:
    base_currency = st.selectbox('Přepočet na', ['USD', 'CZK', 'EUR'], key='base_currency')
st.markdown(f'Aktuální hodnota: {compute.wealth_in_currency(data, base_currency):.2f} {base_currency}')