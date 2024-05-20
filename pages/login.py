import streamlit as st
import streamlit_authenticator as stauth
import auth
from menu import menu

st.title('Přihlášení')

menu()

authenticator = auth.Authenticator()
auth_ui = authenticator.widget
logged_user = authenticator.logged_user()
if logged_user is not None:
    st.write(f'Přihlášen jako: {st.session_state["name"]}')
    col1, col2, spacer = st.columns([1, 1, 3.5])
    with col1:
        if st.button('Změnit heslo'):
            st.switch_page('pages/password_change.py')
    with col2:
        auth_ui.logout('Odhlásit se')
    try:
        if auth_ui.update_user_details(logged_user, fields={'Form name':'Úprava údajů', 'Field': 'Údaj', 'New value': 'Nová hodnota', 'Name':'Jméno', 'Email':'Email', 'Update':'Uložit'}):
            authenticator.save_changes()
            st.success('Údaje byly úspěšně změněny')
    except stauth.UpdateError as e:
        if e.message == 'Email is not valid':
            st.error('Email není ve správném formátu')
        elif e.message == 'New and current values are the same':
            st.warning('Nová hodnota je stejná jako stará')
        else:
            st.error(e.message)
else:
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
        st.session_state['logout'] = None
    auth_ui.login()
    status = st.session_state.get('authentication_status', None)
    if status is None:
        st.warning('Zadejte své uživatelské jméno a heslo')
    elif status is False:
        st.error('Login/heslo nejsou správné')
    else:
        st.write(f'Přihlášen jako *{st.session_state["name"]}*')
        auth_ui.logout()
    