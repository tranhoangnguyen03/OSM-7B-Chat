from openai import OpenAI
from components.chat_formatter import ChatFormatter
from components.utils import st_capture
import streamlit as st
from loguru import logger
from retry import retry

class ChatSession:
    def __init__(self, model_name:str, base_url:str=None):
        self.chat_formatter = ChatFormatter(model_name)
        self.conversation_history = []
        self.client = self.get_client(base_url)
        self.model = model_name

    def get_client(self, base_url):
        assert base_url is not None, "Please provide a base url"
        return OpenAI(
            api_key= 'fakekey',
            base_url= base_url
        )

    def chat(self, message:str, system_prompt:str):
        new_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        formatted_messages = self.chat_formatter.apply_chat_template(
            self.conversation_history[-10:] + new_messages
        )
        logger.debug(formatted_messages)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            stream=True,
            max_tokens=4000
        )
        full_response = []

        # Iterate through API response chunks
        for chunk in response:
          # Get generated text delta since previous chunk & replace <INST> tags with emojis
          delta = chunk.choices[0].delta.content
          # Accumulate delta text from each chunk
          if delta is not None: full_response.append(delta)
          # print to stream stdout to be picked up by UI
          print(delta)
        full_response = self.chat_formatter.replace_inst_tags_with_emoji(''.join(full_response))

        self.conversation_history+= [    
            {"role": "user", "content": message},
            {"role": "assistant", "content": full_response }
        ]

        return full_response
    
    @retry(tries=5, delay=0.2, backoff=2)
    def generate_chat_response(self, message, system_prompt):
        try:
            with st.spinner('Generating response'):
                output_area = st.empty()

                with st_capture(output_area.info):
                    full_response = self.chat(message, system_prompt)

                output_area.empty()
                return full_response
        except Exception as e:
            logger.error(f"Error in generate_chat_response: `{e}` ")
            raise        
        

