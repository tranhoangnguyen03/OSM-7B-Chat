import streamlit as st
from components.models import supported_models, retrieve_model_name
from components.utils import is_valid_url, is_valid_custom_model
from components.session_states import init_chat_session

def st_sidebar():
    with st.sidebar:
        session_settings()
        about_the_app()    

def about_the_app():            
    st.markdown("---")

    with st.expander("### About The App"):
        st.markdown("""
        This app provides a test bed for a variety of Mistral models. These models are small and can be deployed easily on Google Colab for no cost. Use this app to quickly test them out!
                    
        Should you have any queries or suggestions, feel free to raise an issue on the project [GitHub repository](https://github.com/tranhoangnguyen03/OSM-7B-Chat) or send me an [email](tranhoangnguyen03@gmail.com).
        
        Thank you and have fun!
        """)

def session_settings():
    with st.expander("### Settings", expanded= (st.session_state['api_endpoint'] is None)):
        # Select a model
        selected_model= st.selectbox(
            'Choose a supported model:'
            ,['Select a model'] + list(supported_models.keys())
            ,placeholder='Select a model'
        )
        if selected_model !='Select a model':
            # Display instructions to initialize the model
            st.info(
                f"Visit the [link]({supported_models[selected_model]}) and initiate the model "
                "(follow instructions and run cells)."
            ) 
            
            # In case user want to run custom model name    
            custom_model_name = None
            if selected_model == 'Custom Model':
                custom_model_name = set_custom_model()
                is_valid_custom_model(custom_model_name)
            
            # Specify custom model API Endpoint
            api_endpoint = st.text_input('Enter your model API Endpoint', )    

            left, right = st.columns([5,5])  
            with left:        
                model_submitted = st.button(label='Submit API', use_container_width=True)
            with right:
                reset_chat_session = None
                if st.session_state['chat_session']:
                    reset_chat_session = st.button(label='Reset Chat', use_container_width=True)
            if model_submitted:
                initialize_chat_session(api_endpoint, selected_model, custom_model_name)
                init_chat_session()
            elif reset_chat_session:
                initialize_chat_session(api_endpoint, selected_model, custom_model_name)
                init_chat_session(forced=True)

def set_custom_model():   
    # Specify custom model name
    custom_model_name = st.text_input(
        'Enter your model name', placeholder='<creator_name>/<model_name>'
    )
    st.info(
        'We only support HuggingFace models. Specify your model name in the format of '
        '`<creator_name>/<model_name>`.'
    )
    return custom_model_name

def initialize_chat_session(api_endpoint, selected_model, custom_model_name):
    try:
        if is_valid_url(api_endpoint):
            model_actual_name = retrieve_model_name(api_endpoint) 
            if selected_model != 'Custom Model':
                assert model_actual_name == selected_model ,(
                    f"API reports a different model name *`({model_actual_name})`* than provided  *`({selected_model})`* "
                )
            else:
                assert model_actual_name == custom_model_name ,(
                    f"API reports a different model name *`({model_actual_name})`* than provided  *`({custom_model_name})`* "
                ) 
                assert is_valid_custom_model()

            # st.session_state['selected_model'] = custom_model_name or selected_model
            st.session_state['api_endpoint'] = api_endpoint.strip('/') 
            st.session_state['selected_model'] = model_actual_name  

            st.session_state['chat_ready'] = True

    except AssertionError as e:
        st.error(f"{e}. Please check your model API Endpoint and try again.")
        st.session_state['chat_ready'] = False
    except ValueError as e:
        st.error(f"{e}. Please check your model API Endpoint and try again.")
        st.session_state['chat_ready'] = False

