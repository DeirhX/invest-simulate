import streamlit as st
from menu import menu
from data import get_investments

st.set_page_config(page_title='Nákup akcií', layout='centered')
st.subheader('Nákup / prodej akcií')
menu() 

data = get_investments()