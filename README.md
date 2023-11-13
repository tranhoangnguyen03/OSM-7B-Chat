# OSM-7B-Chat

This is an interactive chat app built with Streamlit to demonstrate conversational AI models. 

## Features

- Select from a variety of OpenAI Codex models like Mistral, Jurassic, Davinci etc.
- Interactively chat with the selected AI assistant 
- View chat history and have contextual conversations
- Customize the AI assistant prompt
- Define a response schema for the AI to follow

## Usage

To run the app:
```streamlit run app.py```

This will launch the Streamlit app on http://localhost:8501.

Select a model, deploy on Colab, and start chatting!

## Implementation 

The key components of the app:

- `st_sidebar.py` - Handles model selection and app settings
- `st_main.py` - Renders the chat UI with Streamlit components 
- `openai_client.py` - Wraps the OpenAI API for chat completions
- `chat_formatter.py` - Formats messages for the AI assistant  
- `models.py` - Retrieves model metadata from API

The app maintains conversation state and history in Streamlit session state. 

## Contributions

Contributions are welcome! Please open issues and pull requests.

Some ideas for improvements:

- Add more AI models 
- Improve chat formatting
- Persist conversation history
- Add audio input/output