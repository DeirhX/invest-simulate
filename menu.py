import streamlit as st

def menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Přehled")
    st.sidebar.page_link("pages/buy_sell.py", label="Nákupy / prodeje akcií")
    st.sidebar.page_link("pages/trades.py", label="Historie obchodů")
    st.sidebar.page_link("pages/prices.py", label="Ceny akcií")
    st.sidebar.page_link("pages/currencies.py", label="Kurzy měn")
