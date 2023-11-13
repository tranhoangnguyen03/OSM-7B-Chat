import streamlit as st
from components.session_states import init_session_states
from components.st_sidebar import st_sidebar
from components.st_main import st_main
from components.init import init

init()
init_session_states()
st_sidebar()
st_main()