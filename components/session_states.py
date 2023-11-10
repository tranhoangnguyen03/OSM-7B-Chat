import streamlit as st

def init_session_states():
    if 'selected_model' not in st.session_state:
        st.session_state['selected_model'] = None
    if 'api_endpoint' not in st.session_state: 
        st.session_state['api_endpoint'] = None
    if 'custom_model_name' not in st.session_state:
        st.session_state['custom_model_name'] = None