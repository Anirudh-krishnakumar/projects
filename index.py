import streamlit as st
import google.generativeai as genai

st.title("anik_ai")
st.balloons()
genai.configure(api_key='AIzaSyABF7YzFJLziG5IN_LU3IuvgTabzdNLuYE')
text = st.text_input("prompt")
if text:
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    response = chat.send_message(text)
    st.write(response.text)