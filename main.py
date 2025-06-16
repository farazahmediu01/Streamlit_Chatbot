import os
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI

# load .env file.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Get API key from env.


client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


@cl.on_message
async def on_message(prompt: cl.Message):
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You are a helpful Ai assistant."},
            {"role": "user", "content": prompt.content},
        ],
    )
    content = response.choices[0].message.content
    await cl.Message(content=content).send()


# chainlit run api.py
