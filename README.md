# Agentic AI Chatbot

A Streamlit chat application built with LangGraph and LangChain. It supports a
basic conversational chatbot and a web-enabled chatbot that can search the web
using Tavily.

## Screenshot

![Agentic AI Chatbot showing a web-enabled conversation](<Screenshot 2026-10-05 at 9.19.08 PM.png>)

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An OpenAI API key
- A Tavily API key when using **Chatbot With Web**

## Setup and run

From the project root, install the project dependencies:

```bash
uv sync
```

Start the Streamlit app:

```bash
uv run streamlit run src/agenticaichatbot/main.py
```

Streamlit prints a local URL in the terminal (usually
`http://localhost:8501`). Open it in a browser to use the app.

## Using the chat

1. Enter your OpenAI API key in the sidebar and select a model.
2. Select **Basic Chatbot** for a regular conversation, or **Chatbot With Web**
   to enable Tavily web search.
3. For **Chatbot With Web**, enter your Tavily API key in the sidebar.
4. Enter a message in the chat input at the bottom of the page.

Conversation history is kept in the current Streamlit session. It is not
persisted across separate sessions.

## API key safety

Enter API keys in the app's password fields. Do not commit API keys to source
control or share screenshots that reveal them. If a key has been exposed, revoke
it with its provider and create a replacement.
