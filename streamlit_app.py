import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

with st.sidebar:
    st.title('Simple ChatGPT Interface')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your OpenAI API key')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages, stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
st.markdown("""
    <style>
    .css-1v0mbdj {padding: 1rem;}
    .css-12oz5g7 {padding: 1rem;}
    </style>
    """, unsafe_allow_html=True)
