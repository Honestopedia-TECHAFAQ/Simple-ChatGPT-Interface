import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Initialize OpenAI API
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

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to handle image upload
def handle_image_upload(uploaded_file):
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    return image

# Text input for chat messages
prompt = st.chat_input("What is up?")

# Image upload functionality
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if prompt or uploaded_file:
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    if uploaded_file:
        image = handle_image_upload(uploaded_file)
        # Convert image to bytes for sending to OpenAI API
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = buffered.getvalue()
        st.session_state.messages.append({"role": "user", "content": "Uploaded an image"})
        with st.chat_message("user"):
            st.markdown("Uploaded an image")

    # Call OpenAI API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        # Append image data to messages if uploaded
        if uploaded_file:
            messages.append({"role": "user", "content": "data:image/png;base64," + img_str.encode('base64')})

        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages, stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# CSS for user-friendly design
st.markdown("""
    <style>
    .css-1v0mbdj {padding: 1rem;}
    .css-12oz5g7 {padding: 1rem;}
    </style>
    """, unsafe_allow_html=True)
