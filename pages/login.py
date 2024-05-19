import streamlit as st
import streamlit_authenticator as stauth
import auth
from menu import menu

st.title('Přihlášení')

menu()

authicate = auth.state.widget
logged_user = auth.state.logged_user()
if logged_user is not None:
    st.write(f'Přihlášen jako: {logged_user}')
    col1, col2, spacer = st.columns([1, 1, 3.5])
    with col1:
        if st.button('Změnit heslo'):
            st.switch_page('pages/password_change.py')
    with col2:
        authicate.logout('Odhlásit se')
else:
    authicate.login()
    if st.session_state["authentication_status"]:
        st.write(f'Přihlášen jako *{st.session_state["name"]}*')
        authicate.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Login/heslo nejsou správné')
    elif st.session_state["authentication_status"] is None:
        st.warning('Zadejte své uživatelské jméno a heslo')
