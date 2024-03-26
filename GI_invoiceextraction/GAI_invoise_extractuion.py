from dotenv import load_dotenv
load_dotenv()
import streamlit as st
#user interface
import os
from PIL import Image 
#helps to load the image.
import google.generativeai as genai


genai.configure(api_key =os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")
#now we can use this above model

def get_gemini_response(input,image,prompt):  
    response=model.generate_content([input, image[0], prompt]) 
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("no file uploaded")

#setting the streamlit confg.

st.set_page_config(page_title="Gemini ai image extraction")
st.header("Gemini ai image extraction")
input =st.text_input("input prompt:",key="input")

uploaded_file = st.file_uploader("choose an image of the invoice ",  type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None: # if the file is uploaded
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt= """
 extracting the invoice
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("response is")
    st.write(response)

 