import streamlit as st
from menu import menu
from data import get_investments

st.set_page_config(page_title='Historie', layout='centered')
st.subheader('Historie obchodů')
menu()

data = get_investments()
st.dataframe(data.trades, hide_index=True, 
             column_order=['Time', 'Asset', 'Amount', 'Currency', 'Price', 'Proceeds'], 
             column_config={
                    'Time': st.column_config.DatetimeColumn("Čas"),
                    'Asset': st.column_config.TextColumn("Instrument"),
                    'Amount': st.column_config.NumberColumn("Množství", format="%.2f"),
                    'Currency': st.column_config.TextColumn("Měna"),
                    'Proceeds': st.column_config.NumberColumn("Celková cena", format="%.2f"),
                    'Price': st.column_config.NumberColumn("Cena za kus", format="%.2f"),
                    })