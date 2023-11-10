from openai import OpenAI

def get_client(base_url=None):
    assert base_url is not None, "Please provide a base url"
    client = OpenAI(
        api_key= 'fakekey',
        base_url= base_url
    )
    return client

