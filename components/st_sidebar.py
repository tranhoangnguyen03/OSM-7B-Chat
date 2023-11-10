import streamlit as st
from components.models import supported_models

def st_sidebar():
    with st.sidebar:
        
        with st.expander("### Settings", expanded= (st.session_state['api_endpoint'] is None)):
            
            # Select a model
            selected_model= st.selectbox(
                'Choose a supported model:'
                ,['Select a model'] + list(supported_models.keys()) + ['Custom Model']
                ,placeholder='Select a model'
            )
            if selected_model !='Select a model':
                st.markdown(f"Visit the [link]({supported_models[selected_model]}) to initiate the model.")
                if selected_model == 'Custom Model':
                    # Specify custom model name
                    custom_model_name = st.text_input(
                        'Enter your model name',placeholder='<creator_name>/<model_name>'
                    )

                # Specify custom model API Endpoint
                api_endpoint = st.text_input('Enter your model API Endpoint')    

                if api_endpoint:
                    model_submitted = st.form_submit_button(label='Submit')
                    if model_submitted:
                        st.session_state['selected_model'] = selected_model
                        st.session_state['custom_model_name'] = custom_model_name 
                        st.session_state['api_endpoint'] = api_endpoint 
        
        st.markdown("---")

        with st.expander("### About The App"):
            st.markdown("""
            This app ...
                        
            Should you have any queries or suggestions, feel free to raise an issue on the project [GitHub repository](https://github.com/tranhoangnguyen03/Pydantic_to_BNF_Grammar) or send me an [email](tranhoangnguyen03@gmail.com).
            
            Thank you and have fun!
            """)
