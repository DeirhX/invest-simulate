import streamlit as st
from menu import menu
from data import get_investments
import ux

st.set_page_config(page_title='Historie', layout='centered')
st.subheader('Historie obchodů')
menu()

data = st.session_state.get('data', None) or get_investments()
st.session_state.data = data

ux.show_trades_dataframe(data.get_trades())