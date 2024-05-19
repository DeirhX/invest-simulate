import streamlit as st
import streamlit_authenticator as stauth
import auth
from menu import menu

st.title('Přihlášení')

menu()

authicate = auth.authenticator()
logged_user = auth.status()
if logged_user is not None:
    st.write(f'Přihlášen jako: {logged_user}')
    authicate.logout()
else:
    authicate.login()
    if st.session_state["authentication_status"]:
        st.write(f'Přihlášen jako *{st.session_state["name"]}*')
        authicate.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Login/heslo nejsou správné')
    elif st.session_state["authentication_status"] is None:
        st.warning('Zadejte své uživatelské jméno a heslo')
