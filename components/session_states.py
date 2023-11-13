import streamlit as st
from components.openai_client import ChatSession
from loguru import logger

def init_session_states():

    variables = [
        'selected_model', 'api_endpoint', 'custom_model_name','system_prompt', 'respose_schema', 'chat_ready', 'chat_session',
    ]

    # Initialize session state variables
    for variable in variables:
        if variable not in st.session_state:
            st.session_state[variable] = None

def init_chat_session(forced=False):
    try:
        if (not st.session_state['chat_session'] and st.session_state['chat_ready']) or forced:
            st.session_state['chat_session'] = ChatSession(
                model_name= st.session_state['selected_model'], 
                base_url= st.session_state['api_endpoint']
            ) 
 
    except Exception as e:
        logger.error(f'Error initializing chat session: {e}')
        raise InterruptedError(f'Error initializing chat session: {e}')
