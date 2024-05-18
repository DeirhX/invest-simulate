import streamlit as st
from menu import menu
from data import get_investments

st.set_page_config(page_title='Kurzy měn', layout='centered')
st.subheader('Aktuální kurzy měn')
menu() 

data = st.session_state.get('data', None) or get_investments()
st.session_state.data = data

st.dataframe(data.currencies.sort_values(by='From') , hide_index=True,
             column_order=['From', 'Price', 'To'], 
             column_config={'From': st.column_config.TextColumn("Za"),
                            'To': st.column_config.TextColumn("Čeho"),
                            'Price': st.column_config.NumberColumn("Dostanu", format="%.3f")})