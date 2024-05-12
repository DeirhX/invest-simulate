import streamlit as st

def menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Přehled")
    st.sidebar.page_link("pages/buy_sell.py", label="Nákupy / prodeje akcií")