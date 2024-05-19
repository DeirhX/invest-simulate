import streamlit as st
import streamlit_authenticator as stauth
import auth
from menu import menu

st.title('Přihlášení')

menu()
auth.need_login()

authicate = auth.state.widget
if st.session_state["authentication_status"]:
    try:
        if authicate.reset_password(st.session_state["username"], fields={'Form name':'Změna hesla', 'Current password':'Aktuální heslo', 'New password':'Nové heslo', 'Repeat password': 'Zopakovat heslo', 'Reset':'Změnit'}):
            st.success('Heslo bylo úspěšně změněno')
            auth.state.save_changes()
    except Exception as e:
        st.error(e)
