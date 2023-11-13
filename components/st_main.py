import streamlit as st

import time

def st_main():
    if st.session_state['chat_ready']:
        left, mid = st.columns([3,7])
        with left:
            set_system_prompt()
        with mid:
            render_past_messages()
        with left:
            set_reponse_schema()
            conduct_chat_round()

def render_past_messages():
    with st.container():
        st.caption('Messages History (Reverse Order)')
        chat_history = st.session_state['chat_session'].conversation_history
        if len(chat_history) > 1:
            # Reversed iteration
            for i in range(len(chat_history) - 1, -1, -1):
                msg = chat_history[i]
                # Check if the message is from the assistant
                if msg["role"] == "assistant":
                    # Display user's message first if it exists
                    if i > 0 and chat_history[i - 1]["role"] == "user":
                        user_msg = chat_history[i - 1]
                        st.chat_message(user_msg["role"]).markdown(f'<p>{user_msg["content"]}</p>', True)
                    # Then display assistant's message
                    st.chat_message(msg["role"]).markdown(f'{msg["content"]}')


def set_system_prompt():
    with st.container():
        st.session_state['system_prompt'] = st.text_area(
            label= 'System Message:', 
            value='You are json machine that produce json inputs for other machine downstream. You reply in json only.', 
            key='input_system_prompt',
            height= 200
        )
        st.session_state['system_prompt'] = "This is very important for my career. "+st.session_state['system_prompt']

def set_reponse_schema():
    with st.expander('Response Schema'):
        st.session_state['include_response_schema'] = st.checkbox('Add Response Schema')
        if st.session_state['include_response_schema']:
            response_schema = st.text_area(
                label= 'Response Schema ([BNF Grammar recommended](https://pydantic-2-bnf-grammar.streamlit.app/)):', 
                value=("""root ::= ThoughtAnswerResponse"""  
                    """\nThoughtAnswerResponse ::= '{' ws "thought" ws ":" ws string ws ',' ws "answer" ws ":" ws string ws ',' ws "explanation " ws ":" ws strlist ws '}'  """
                    """\nstring ::= '"' ([^"]*) '"'  """
                    """\nnumber ::= [0-9]+ ('.' [0-9]*)?  """
                    """\ndatetime ::= string  """
                    """\nws ::= [ \\t\\n]*  """
                    """\nboolean ::= 'true' | 'false'  """
                    """\nstringlist ::= '[' ws ']' | '[' ws string (ws ',' ws string)* ws ']'  """
                    """\nnumberlist ::= '[' ws ']' | '[' ws number (ws ',' ws number)* ws ']'"""
                ), 
                key='input_response_schema',
                height= 200
            )
            st.session_state['response_schema'] = f"Your json reply follows this schema: ```{response_schema}```"

def conduct_chat_round():
    with st.container():
        user_input = st.empty()
        submit_button = st.empty()
        # Streamlit app code
        user_message = user_input.text_area("Enter your message:", key='human_message', height= 200)
        submitted = submit_button.button("Send", on_click=clear_text)
        if submitted:
            user_message = st.session_state['temp']
            # Hide the input and submit button while the AI is thinking
            user_input.empty()
            submit_button.empty()

            st.chat_message('user').markdown(f'{user_message}', True)
            
            # Call generate_chat_response method from ChatSession instance
            system_prompt = st.session_state['system_prompt']
            if st.session_state['include_response_schema']:
                system_prompt += st.session_state['response_schema']
            chat_response = st.session_state['chat_session'].generate_chat_response(
                user_message, system_prompt)
            
            # Display or process the chat_response as needed
            st.chat_message('assistant').markdown(f'<p>{chat_response}</p>', True)
            time.sleep(2)
            st.rerun()

def clear_text():
    if "temp" not in st.session_state:
        st.session_state["temp"] = ""
    st.session_state["temp"] = st.session_state["human_message"]
    st.session_state["human_message"] = ""
        