from io import StringIO
from contextlib import contextmanager, redirect_stdout
import re
from transformers import AutoTokenizer
import streamlit as st

# Define a context manager to capture the output of streamlit functions
@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield

def is_valid_url(url):
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    if bool(re.match(pattern, url)):
        return True
    else:
        raise ValueError("Invalid url")

def is_valid_custom_model(model_name):
    try:
        AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        st.error(f"Unable to find the specified model `{model_name}` on https://huggingface.co/models")
