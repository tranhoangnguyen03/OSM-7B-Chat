import streamlit as st

def init():
    st.set_page_config(
        page_title="Chat with OpenSource Models",
        page_icon="🔀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    
    # App Header
def app_header():
    st.title('Chat with OSS Models')
    with st.expander('Welcome!'):
        st.markdown(
            "Welcome to the app!   \n\n"
            "This app gives you a playground to chat with various local models`:  \n"
            "1. Select an available model or input your own. \n"
            "2. A link to a colab notebook will show up. Go to the link and initiate the model. \n"
            "3. Copy and paste the API Endpoint from the link and you can chat with it. \n"
        )


