import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class Authenticator():
    SECRETS_FILE = '.streamlit/auth.yaml'
    
    def __init__(self):
        with open(Authenticator.SECRETS_FILE) as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        self.widget = stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['pre-authorized']
        )

    def logged_user(self):    
        status = st.session_state.get('authentication_status', None)
        if (status is not None):
            return st.session_state["username"]
        return None

    def save_changes(self):
        with open(Authenticator.SECRETS_FILE, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
            
def need_login():
    if not Authenticator().logged_user():
        st.switch_page('pages/login.py')

