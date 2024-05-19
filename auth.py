import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def need_login():
    if not status():
        st.switch_page('pages/login.py')

def authenticator():
    with open('.streamlit/auth.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )
    return authenticator

def status():    
    status = st.session_state.get('authentication_status', None)
    if (status is not None):
        return st.session_state["username"]
    return None
    # authenticator.login()