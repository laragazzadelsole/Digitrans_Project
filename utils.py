import streamlit as st

def initialize_session_state():
        # Initializing utility state variables
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''

        # Setting initialized state as true so that we don't reinitialize every time
        st.session_state['initialized'] = True
    
def save_input_to_session_state(key, value):
    ## Helper function to save input into session state.
    st.session_state[key] = value

def safe_var(key):
    # Return None without breaking if asked for a var which is not there
    if key in st.session_state:
        return st.session_state[key]
    return None