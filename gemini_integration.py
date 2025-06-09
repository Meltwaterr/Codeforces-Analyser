# gemini_integration.py

import streamlit as st
import google.generativeai as genai

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text
    except Exception as e:
        return f"An error occurred with the Gemini API: {e}"

def initialize_chat(context):
    initial_prompt = f"You are an expert competitive programming AI assistant. The user has a question regarding the following context. Your task is to answer their questions concisely and accurately.\n\n---CONTEXT---\n{context}\n---END CONTEXT---\n\nNow, please answer the user's question."
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.start_chat(history=[{'role': 'user', 'parts': [initial_prompt]}, {'role': 'model', 'parts': ["Understood. I am ready to assist with this context. What is your question?"]}])

def display_chat_interface(chat_key):
    if f"chat_session_{chat_key}" not in st.session_state:
        st.error("Chat session not found.")
        return
    for message in st.session_state[f"chat_session_{chat_key}"].history[2:]:
        with st.chat_message(name=message.role, avatar="🧑‍💻" if message.role == "user" else "🤖"):
            st.markdown(message.parts[0].text)
    if prompt := st.chat_input("Ask a follow-up question..."):
        with st.chat_message(name="user", avatar="🧑‍💻"):
            st.markdown(prompt)
        with st.spinner("🤖 Thinking..."):
            response = st.session_state[f"chat_session_{chat_key}"].send_message(prompt)
            with st.chat_message(name="model", avatar="🤖"):
                st.markdown(response.text)