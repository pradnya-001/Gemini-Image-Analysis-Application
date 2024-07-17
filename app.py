from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Google API key is not set in the environment variables.")

# Define the function to get the Gemini response
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Streamlit app setup
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# Input prompt
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button to get the response
submit = st.button("Tell me about the image")
if submit:
    if image is not None:
        response = get_gemini_response(input_text, image)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload an image to get a response.")
