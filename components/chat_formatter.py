from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

def generate_knowledge_graph(topic, context='None'):
    return (
        "create a Python program that: \n"
        "- takes in a key phrase and a list of site exclusions \n"
        "- outputs a list of 10 most relevant links plus their descriptions"
    )

topic = 'Human-led AI workforce'
context = "My career depends on this."
user_prompt = generate_knowledge_graph(topic, context)

messages = [
    {
        "role": "user",
        "content": 'You are a Python coder ' + user_prompt
    }
]

encodeds = tokenizer.apply_chat_template(
    messages, tokenize=False, return_tensors="pt"
)

encodeds