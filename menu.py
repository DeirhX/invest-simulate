import streamlit as st
import auth

def menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("pages/overview.py", label="Přehled")
    st.sidebar.page_link("pages/buy_sell.py", label="Nákupy / prodeje akcií")
    st.sidebar.page_link("pages/trades.py", label="Historie obchodů")
    st.sidebar.page_link("pages/prices.py", label="Ceny akcií")
    st.sidebar.page_link("pages/currencies.py", label="Správa / výměna měn")
    st.sidebar.page_link("pages/login.py", label="Účet")

