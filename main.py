import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.title("ChatGPT-like clone")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

st.session_state.setdefault("messages", [])

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
if prompt := st.chat_input("Type your prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            stream=True,
            messages=st.session_state.messages,
        )

        def stream():
            full = ""
            for chunk in response:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    full += delta
                    yield delta
            st.session_state.messages.append({"role": "assistant", "content": full})

        st.write_stream(stream())
