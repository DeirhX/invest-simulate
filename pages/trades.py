import streamlit as st
from menu import menu
from data import get_investments
import ux

st.set_page_config(page_title='Historie', layout='centered')
st.subheader('Historie obchodů')
menu()

data = get_investments()
ux.show_trades_dataframe(data.trades)